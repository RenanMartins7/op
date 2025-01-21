from fastapi import FastAPI, Query
from merge import *
from selection import *
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



