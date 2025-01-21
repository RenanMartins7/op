import iperf3

def start_iperf_server(port=5201):
    server = iperf3.Server()
    server.port = port

    print(f"Servidor iPerf3 iniciado na porta {port}. Aguardando conexões...")
    try:
        while True:
            result = server.run()
            if result:
                print(f"Cliente conectado: {result.remote_host}")
                print(f"Largura de banda recebida: {result.received_Mbps} Mbps")
                print(f"Largura de banda enviada: {result.sent_Mbps} Mbps")
    except KeyboardInterrupt:
        print("\nServidor iPerf3 encerrado.")
    except Exception as e:
        print(f"Erro no servidor: {e}")

# Exemplo de uso
if __name__ == "__main__":
    start_iperf_server()