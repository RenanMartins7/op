from fastapi import FastAPI, Query
from merge import *
from selection import *
from iperf import *
from otlp_provider import *
from metrics import *
import random

from opentelemetry.sdk.resources import SERVICE_NAME, Resource

resource = Resource(attributes={SERVICE_NAME: "api"})
os.environ["OTEL_SERVICE_NAME"] = "api"

#-----------------------------------------Traces, metrics and app service creation-------------------------
tracer = traces_provider(resource)
meter = metrics_provider(resource)
metrics = prometheus_metrics(meter)
app = FastAPI()



#-----------------------------------------Services Implementation------------------------------------------
#-----------------------------------------------Merge Sort-------------------------------------------------
@app.get("/merge")
def merge_service(size: int = Query(10000, ge=1)):

    metrics.total_requests_add(1, "/merge")
    metrics.active_requests_add(1)

    with tracer.start_as_current_span("mergesort", kind=trace.SpanKind.SERVER) as child:

        random_list = [random.randint(1, size) for _ in range(size)]
        merge_sort(random_list)
        child.set_attribute("teste", 12)
    
    metrics.active_requests_add(-1)
    return {"message": "Merge sort completed"}

#-----------------------------------------------Selection Sort------------------------------------------------
@app.get("/selection")
def selection_service(size: int= Query(10000, ge=1)):

    metrics.total_requests_add(1, "/selection")
    metrics.active_requests_add(1)

    with tracer.start_as_current_span("selectionsort", kind=trace.SpanKind.SERVER) as child:

        random_list = [random.randint(1, size) for _ in range(size)]
        selection_sort(random_list)

    metrics.active_requests_add(-1)
    return {"message": "Selection sort completed"}

#---------------------------------------------------Iperf-----------------------------------------------------
@app.get("/iperftest")
def iperf_service(server: str = Query("0.0.0.0"), port: int = Query(5201, ge=1), duration: int = Query(10, ge=1)):
    
    metrics.total_requests_add(1, "/iperf")
    metrics.active_requests_add(1)

    with tracer.start_as_current_span("iperf", kind=trace.SpanKind.SERVER) as child:

        run_iperf(server, port, duration)
    
    metrics.active_requests_add(-1)
    return {"message": "Iperf test completed"}