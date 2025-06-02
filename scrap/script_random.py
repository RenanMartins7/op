import requests
import concurrent.futures
import random

URL = "http://api:8000/merge"
NUM_REQUESTS = 10    # Número de requisições concorrentes
NUM_SERIAL = 40000   # Número total de requisições (executadas em lotes)

def make_request():
    try:
        list_size = random.randint(1, 5000)

        payload = {
            "array": [random.randint(1, list_size) for _ in range(list_size)],
            "index": random.randint(1, list_size),
            "userId": random.randint(1, list_size)
        }

        response = requests.post(URL, json=payload)
        #print(f"Status: {response.status_code} | Response: {response.json()}")
    except Exception as e:
        print(f"Erro: {e}")

with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_REQUESTS) as executor:
    for _ in range(NUM_SERIAL):
        executor.map(lambda _: make_request(), range(NUM_REQUESTS))
