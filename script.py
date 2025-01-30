import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

# URLs que serão acessadas
urls = [
    "http://api:8000/selection?size=3000",
    "http://api:8000/merge",
    #"http://localhost:8000/iperftest?server=143.54.201.115&duration=2"
]

# Função para fazer a requisição HTTP
def fetch_url(url):
    try:
        response = requests.get(url)
        return url, response.status_code, response.text
    except requests.RequestException as e:
        return url, None, str(e)

# Número de requisições paralelas
num_requests = 20

# Lista para armazenar os resultados
results = []

# Usando ThreadPoolExecutor para fazer as requisições de forma paralela
with ThreadPoolExecutor(max_workers=num_requests) as executor:
    # Criando uma lista de futures para cada URL
    futures = [executor.submit(fetch_url, url) for url in urls * num_requests]

    # Coletando os resultados conforme as requisições são completadas
    for future in as_completed(futures):
        url, status_code, content = future.result()
        results.append((url, status_code, content))
        print(f"URL: {url}, Status Code: {status_code}, Content: {content[:100]}...")  # Exibe os primeiros 100 caracteres do conteúdo

# Exibindo um resumo dos resultados
print("\nResumo das requisições:")
for url in urls:
    count = sum(1 for result in results if result[0] == url)
    print(f"{url}: {count} requisições completadas")