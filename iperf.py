import iperf3

def run_iperf(server, port=5201, duration=10):
    client = iperf3.Client()
    client.server_hostname = server
    client.port = port
    client.duration = duration

    print(f"Conectando ao servidor {server}:{port}...")

    result = client.run()

    if result.error:
        print(f"Erro: {result.error}")
        return None
    
    print(f"Largura de banda: {result.sent_Mbps} Mbps")
    return result