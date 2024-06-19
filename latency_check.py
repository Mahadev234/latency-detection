import asyncio
import websockets
import time
import socket
from urllib.parse import urlparse
import os


async def websocket_latency_test(uri, num_tests=10):
    latencies = []
    async with websockets.connect(uri) as websocket:
        for _ in range(num_tests):
            start_time = time.time()
            await websocket.send("ping")
            await websocket.recv()
            end_time = time.time()
            latencies.append((end_time - start_time) * 1000)
    return latencies


def tcp_handshake_latency(host, port):
    try:
        start_time = time.perf_counter()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        end_time = time.perf_counter()
        s.close()
        return (end_time - start_time) * 1000
    except Exception as e:
        print(f"Error measuring TCP handshake latency: {e}")
        return None


async def main():
    websocket_uri = f"ws://{os.environ.get('WS_SERVER', 'websocket-server')}:{os.environ.get('WS_PORT', 8081)}"
    target_website = os.environ.get("TARGET_WEBSITE", "node-app:8080")
    test_url = f"http://{target_website}"

    websocket_latencies = await websocket_latency_test(websocket_uri)
    parsed_url = urlparse(test_url)
    tcp_latency = tcp_handshake_latency(parsed_url.hostname, parsed_url.port)

    print("\nWebSocket Latencies (ms):", websocket_latencies)
    print(f"\nTCP Handshake Latency (ms): {tcp_latency}")

    if tcp_latency is not None:
        # Basic proxy detection (customize this logic further)
        avg_ws_latency = sum(websocket_latencies) / len(websocket_latencies)
        if avg_ws_latency - tcp_latency > 50:  # Threshold (adjust as needed)
            print("Potential proxy detected!")
        else:
            print("Direct connection likely.")
    else:
        print("Could not determine connection type due to TCP error.")


if __name__ == "__main__":
    asyncio.run(main())
