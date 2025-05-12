from fastapi import Request, FastAPI
from otlp_provider import *
from metrics import *
from pydantic import BaseModel
from typing import List
import random
import requests

from opentelemetry import baggage
from opentelemetry.trace import SpanKind
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator

from opentelemetry import metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

# Configuração do coletor
resource = Resource(attributes={SERVICE_NAME: "binary-search"})
os.environ["OTEL_SERVICE_NAME"] = "binary-search"

tracer = traces_provider(resource)  # Instância do tracer
meter = metrics_provider(resource)
p_metrics = prometheus_metrics(meter)

app = FastAPI()

class SearchRequest(BaseModel):
    data: List[int]
    userId: int

# Função de busca binária
def busca_binaria(lista, elemento):
    inicio = 0
    fim = len(lista) - 1
    
    while inicio <= fim:
        meio = (inicio + fim) // 2  
        
        if lista[meio] == elemento:
            return meio  
        elif lista[meio] < elemento:
            inicio = meio + 1 
        else:
            fim = meio - 1 
    
    return -1  # Retorna -1 se o elemento não for encontrado

@app.post("/binary_search")
async def busca_binaria_endpoint(request: Request, body: SearchRequest):
    # Extraindo os headers recebidos
    headers = dict(request.headers)
    print("\nbinary")

    # Propagação do contexto de tracing e baggage
    ctx = TraceContextTextMapPropagator().extract(headers)
    baggage_ctx = W3CBaggagePropagator().extract(headers)

    # Criando um span filho do trace recebido
    with tracer.start_as_current_span("binary_search", context=ctx, kind=SpanKind.SERVER) as span:

        # Recuperando possíveis valores da baggage
        merge_info = baggage.get_baggage("merge", context=baggage_ctx)
        if merge_info:
            span.set_attribute("baggage.merge", merge_info)

        # Obtendo a lista ordenada do corpo da requisição
        orderedList = body.data

        #Obtendo o userId
        userId = body.userId

        # Selecionando um elemento aleatório para busca
        element = random.randint(1, len(orderedList))

        # Executando a busca binária
        found_index = busca_binaria(orderedList, element)
        span.set_attribute("found_index", found_index)
        if(found_index == -1):
            result = found_index
        else:
            ctx = baggage.set_baggage("binary", "teste")
            headers = {}
            W3CBaggagePropagator().inject(headers, ctx)
            TraceContextTextMapPropagator().inject(headers, ctx)
            # Retornando o resultado da busca
            url = "http://register:8002/register"
            response = requests.post(url, json={"data": found_index, "userId": userId}, headers=headers)
            result = response.json()
        
 
    return {"result": result}
