import requests
import concurrent.futures
import json

URL = "http://localhost:8000/merge"
MAX_WORKERS = 1  # Número de requisições concorrentes

# Carrega os dados do arquivo
with open("dados.json", "r") as f:
    entradas = json.load(f)

# Função que envia uma única requisição com uma entrada
def make_request(payload):
    try:
        response = requests.post(URL, json=payload)
    except Exception as e:
        print(f"Erro ao enviar userId={payload['userId']}: {e}")

# Executa as requisições com paralelismo, mas sem repetir entrada
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    executor.map(make_request, entradas)
