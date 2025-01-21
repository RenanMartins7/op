from fastapi import FastAPI, Query
from merge import *
from selection import *
from iperf import *
import random

app = FastAPI()

@app.get("/merge")
def merge_service(size: int = Query(10000, ge=1)):
    random_list = [random.randint(1, size) for _ in range(size)]
    merge_sort(random_list)
    return {"message": "Merge sort completed"}

@app.get("/selection")
def selection_service(size: int= Query(10000, ge=1)):
    random_list = [random.randint(1, size) for _ in range(size)]
    selection_sort(random_list)
    return {"message": "Selection sort completed"}

@app.get("/iperftest")
def iperf_service(server: str = Query("0.0.0.0"), port: int = Query(5201, ge=1), duration: int = Query(10, ge=1)):
    run_iperf(server, port, duration)