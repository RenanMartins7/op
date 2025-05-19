import json
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib

# === 1. Leitura e pré-processamento ===

# Carrega o arquivo JSON
with open("traces.json") as f:
    data = json.load(f)

# Converte para DataFrame
df = pd.DataFrame(data)

# Remove coluna artificial_error se existir
df = df.drop(columns=["artificial_error"], errors="ignore")

# Mantém apenas as colunas numéricas ou codificáveis
# Vamos codificar `operationName` e `baggage.merge` (se presente)
df["operationName"] = df["operationName"].astype("category").cat.codes

if "baggage.merge" in df.columns:
    df["baggage.merge"] = df["baggage.merge"].astype("category").cat.codes

# Preenche valores ausentes com 0 (ou use outra estratégia se preferir)
df = df.fillna(0)

# Define as features de entrada
features = ["startTime", "duration", "operationName"]

# Adiciona colunas extras, se existirem
extra_cols = [col for col in ["List Size", "found_index", "baggage.merge"] if col in df.columns]
features += extra_cols

X = df[features]

# Normaliza os dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# === 2. Treina a Isolation Forest ===
model = IsolationForest(
    n_estimators=500,           # mais árvores => melhor generalização (padrão: 100)
    max_samples='auto',         # ou um número fixo (ex: 512, 2048)
    contamination='auto',       # ou um valor fixo (ex: 0.01 para 1% de outliers)
    max_features=1.0,           # fração de features a considerar por split
    bootstrap=False,
    random_state=42,
    n_jobs=-1                   # usa todos os núcleos de CPU
)
model.fit(X_scaled)

# Calcula score de anomalia
df["anomaly_score"] = model.decision_function(X_scaled)
df["is_outlier"] = model.predict(X_scaled)  # -1 = outlier, 1 = normal

# === 3. Resultados ===
# Exibe os possíveis outliers
outliers = df[df["is_outlier"] == -1]
print(outliers[["traceID", "spanID", "operationName", "anomaly_score"]])

# Salva o resultado em JSON
df.to_json("traces_com_anomalias.json", orient="records", indent=2)


joblib.dump(model, "isolation_forest_model.joblib")

joblib.dump(scaler, "scaler.joblib")