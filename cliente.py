import socket
import json

host = 'localhost'
port = 5000

mensaje = {"id": "sensor_4", "valor": 73.2, "timestamp": "2025-05-30T14:22:11"}

def enviar_mensaje(mensaje):
    print("[CLIENTE] Conectando al servidor...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        data = json.dumps(mensaje).encode('utf-8')
        print(f"[CLIENTE] Enviando mensaje: {data}")
        client_socket.sendall(data)
        
        respuesta = client_socket.recv(1024)
        print("[CLIENTE] Respuesta del servidor:", respuesta.decode('utf-8'))

# Ejecuta el envío
enviar_mensaje(mensaje)

