import requests
import json

# Configurações
ES_URL = "http://localhost:9200/jaeger-span-*/_search?scroll=2m"
SCROLL_URL = "http://localhost:9200/_search/scroll"
HEADERS = {"Content-Type": "application/json"}
BATCH_SIZE = 1000  # número de documentos por lote
operations = ["mergesort", "binary_search", "register"]
excluded_tags = {"internal.span.format", "otel.scope.name", "span.kind"}

flattened_data = []

# Passo 1: primeira busca com scroll
initial_query = {
    "size": BATCH_SIZE,
    "_source": True,
    "query": {
        "terms": {
            "operationName": operations
        }
    }
}

res = requests.post(ES_URL, headers=HEADERS, data=json.dumps(initial_query))
data = res.json()
scroll_id = data.get('_scroll_id')
spans = data.get('hits', {}).get('hits', [])

def process_spans(spans):
    result = []
    for span in spans:
        src = span['_source']
        flat_span = {
            "traceID": src.get("traceID"),
            "spanID": src.get("spanID"),
            "startTime": src.get("startTime"),
            "duration": src.get("duration"),
            "operationName": src.get("operationName")
        }

        for tag in src.get("tags", []):
            key = tag.get("key")
            if key not in excluded_tags:
                flat_span[key] = tag.get("value")

        result.append(flat_span)
    return result

flattened_data.extend(process_spans(spans))

# Passo 2: continuar buscando até acabar
loopBreaker = True
while loopBreaker:
    if not spans:
        break

    scroll_payload = {
        "scroll": "2m",
        "scroll_id": scroll_id
    }

    res = requests.post(SCROLL_URL, headers=HEADERS, data=json.dumps(scroll_payload))
    data = res.json()
    scroll_id = data.get('_scroll_id')
    spans = data.get('hits', {}).get('hits', [])

    flattened_data.extend(process_spans(spans))


# Salva os dados processados no arquivo JSON
with open("traces.json", "w") as f:
    json.dump(flattened_data, f, indent=2)

print(f"Total de spans coletados: {len(flattened_data)}")
