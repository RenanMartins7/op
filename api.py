from fastapi import FastAPI, Query, Request
import requests
from merge import *
from selection import *
from iperf import *
from otlp_provider import *
from metrics import *
import json

from opentelemetry import metrics

from opentelemetry import baggage
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.baggage.propagation import W3CBaggagePropagator


import random

from typing import Iterable

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

resource = Resource(attributes={SERVICE_NAME: "api"})
os.environ["OTEL_SERVICE_NAME"] = "api"

#-----------------------------------------Traces, metrics and app service creation-------------------------
tracer = traces_provider(resource)
meter = metrics_provider(resource)
p_metrics = prometheus_metrics(meter)
app = FastAPI()



#-----------------------------------------Services Implementation------------------------------------------
#-----------------------------------------------Merge Sort-------------------------------------------------
@app.get("/merge")
def merge_service(size: int = Query(10000, ge=1)):
    p_metrics.total_requests_add(1, "/merge")

    with tracer.start_as_current_span("mergesort", kind=trace.SpanKind.SERVER) as parent:

        random_list = [random.randint(1, size) for _ in range(size)]
        orderedList = merge_sort(random_list)

        ctx = baggage.set_baggage("merge", "teste")
        headers = {}
        W3CBaggagePropagator().inject(headers, ctx)
        TraceContextTextMapPropagator().inject(headers, ctx)

        url = "http://binary:8001/binary_search"
        
        response = requests.post(url, json={"data": orderedList}, headers=headers)



    return {"message": "Merge sort completed"}

#-----------------------------------------------Selection Sort------------------------------------------------
# @app.get("/selection")
# def selection_service(size: int= Query(10000, ge=1)):
#     p_metrics.total_requests_add(1, "/selection")

#     with tracer.start_as_current_span("selectionsort", kind=trace.SpanKind.SERVER) as child:
#         random_list = [random.randint(1, size) for _ in range(size)]
#         selection_sort(random_list)

#     return {"message": "Selection sort completed"}

# #---------------------------------------------------Iperf-----------------------------------------------------
# # @app.get("/iperftest")
# # def iperf_service(server: str = Query("0.0.0.0"), port: int = Query(5201, ge=1), duration: int = Query(10, ge=1)):
# #     p_metrics.total_requests_add(1, "/iperf")
    
# #     with tracer.start_as_current_span("iperf", kind=trace.SpanKind.SERVER) as child:
# #         run_iperf(server, port, duration)
    
# #     return {"message": "Iperf test completed"}

# #------------------------------------------------MiddleWare for active requests--------------------------------
@app.middleware("http")
async def count_active_requests(request:Request, call_next):
    p_metrics.active_requests_add(1)
    response = await call_next(request)
    p_metrics.active_requests_add(-1)

    return response
    