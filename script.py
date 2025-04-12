import requests
import concurrent.futures

URL = "http://localhost:8000/merge"
NUM_REQUESTS = 20   # Número de requisições concorrentes
NUM_SERIAL = 100      # Número de requisições seriais

def make_request():
    try:
        response = requests.get(URL)
        #print(f"Status Code: {response.status_code}")
    except Exception as e:
        print(f"Erro: {e}")

with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_REQUESTS) as executor:

    for _ in range(NUM_SERIAL):
        executor.map(lambda _: make_request(), range(NUM_REQUESTS))
