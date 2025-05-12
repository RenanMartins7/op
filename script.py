import requests
import concurrent.futures
import random

URL = "http://localhost:8000/merge"
NUM_REQUESTS = 3    # Número de requisições concorrentes
NUM_SERIAL = 40000  # Número de requisições seriais

def make_request():
    try:
        size = random.randint(1, 10000)
        params = {"size": size}
        response = requests.get(URL, params=params)
        #print(f"Requisição com size={size} => Status: {response.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_REQUESTS) as executor:
    for _ in range(NUM_SERIAL):
        executor.map(lambda _: make_request(), range(NUM_REQUESTS))

