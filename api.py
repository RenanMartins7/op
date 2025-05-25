from fastapi import FastAPI, Request
from fastapi import Query
from fastapi import Body
import requests
from merge import *
from selection import *
from iperf import *
from otlp_provider import *
from metrics import *
import json

from opentelemetry import metrics, trace, baggage
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator

import os
from typing import List
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from pydantic import BaseModel

resource = Resource(attributes={SERVICE_NAME: "api"})
os.environ["OTEL_SERVICE_NAME"] = "api"

# Traces, metrics, and app
tracer = traces_provider(resource)
meter = metrics_provider(resource)
p_metrics = prometheus_metrics(meter)
app = FastAPI()

# Request model
class SearchRequest(BaseModel):
    array: List[int]
    index: int
    userId: int

# POST /merge: recebe dados e repassa ao serviço /binary_search
@app.post("/merge")
def merge_service(payload: SearchRequest):
    p_metrics.total_requests_add(1, "/merge")

    size = len(payload.array)
    with tracer.start_as_current_span(
        "mergesort", 
        kind=trace.SpanKind.SERVER, 
        attributes={"List Size": size, "userId": payload.userId, "index": payload.index}
    ) as parent:

        # Adiciona erro artificial se múltiplo de 501
        if size % 501 == 0:
            orderedList = payload.array
            parent.set_attribute("artificial_error", 1)
        else:
            orderedList = merge_sort(payload.array)

        # Propagação de contexto
        ctx = baggage.set_baggage("merge", "success")
        headers = {}
        W3CBaggagePropagator().inject(headers, ctx)
        TraceContextTextMapPropagator().inject(headers, ctx)

        # Envia para serviço /binary_search
        url = "http://binary:8001/binary_search"
        response = requests.post(url, json={
            "array": orderedList,
            "index": payload.index,
            "userId": payload.userId
        }, headers=headers)

    return {"message": "Merge sort completed"}
