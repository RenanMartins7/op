import requests
import json

# Operações desejadas
operations = ["mergesort", "binary_search", "register"]

# Tags que serão ignoradas
excluded_tags = {"internal.span.format", "otel.scope.name", "span.kind"}

# Consulta no Elasticsearch
res = requests.post(
    "http://elasticsearch:9200/jaeger-span-*/_search",
    headers={"Content-Type": "application/json"},
    data=json.dumps({
        "query": {
            "terms": {
                "operationName": operations
            }
        },
        "size": 120000
    })
)

spans = res.json().get('hits', {}).get('hits', [])

# Monta o dicionário final com tags achatadas e operationName
flattened_data = []
for span in spans:
    src = span['_source']
    
    flat_span = {
        "traceID": src.get("traceID"),
        "spanID": src.get("spanID"),
        "startTime": src.get("startTime"),
        "duration": src.get("duration"),
        "operationName": src.get("operationName")
    }

    # Adiciona tags como campos diretos (ignorando as excluídas)
    for tag in src.get("tags", []):
        key = tag.get("key")
        if key not in excluded_tags:
            flat_span[key] = tag.get("value")

    flattened_data.append(flat_span)

# Salva no arquivo JSON
with open("traces.json", "w") as f:
    json.dump(flattened_data, f, indent=2)

    
