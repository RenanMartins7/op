from fastapi import Request, FastAPI
from otlp_provider import *
from metrics import *
from pydantic import BaseModel
from typing import List
import random

from opentelemetry import baggage
from opentelemetry.trace import SpanKind
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator

from opentelemetry import metrics
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


# Configuração do coletor
resource = Resource(attributes={SERVICE_NAME: "register"})
os.environ["OTEL_SERVICE_NAME"] = "register"

tracer = traces_provider(resource)  # Instância do tracer
meter = metrics_provider(resource)
p_metrics = prometheus_metrics(meter)

app = FastAPI()

registerList = []

class SearchRequest(BaseModel):
    data: int
    userId: int


@app.post("/register")
async def register_endpoint(request: Request, body: SearchRequest):
    headers = dict(request.headers)
    
    ctx = TraceContextTextMapPropagator().extract(headers)
    baggage_ctx = W3CBaggagePropagator().extract(headers)

    element = body.data
    userId = body.userId

    with tracer.start_as_current_span("register", context=ctx, kind=SpanKind.SERVER) as span:
        try:
            # Colocado aqui o erro proposital para treinar a IA
            if userId >= 2000 or userId <= 1000:
                registerList.append(element)
            # Colocando aqui código de erro forçado
            elif element % 2345 == 0:
                span.set_attribute("index_2345_error", 1)
                _ = element / 0  # força divisão por zero
                # registerList.append(element)
            else:
                span.set_attribute("userId_error", 1)

            return {"status": "ok"}

        except ZeroDivisionError as e:
            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
            return {"error": "Erro interno: divisão por zero"}, 500
