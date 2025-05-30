import socket
import threading
import os
import json
import csv

def manejar_cliente(conn, addr, lock, archivo_csv):
    print(f"[+] Conexión establecida con {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                print(f"[i] Cliente {addr} cerró conexión.")
                break
            try:
                print(f"[DEBUG] Mensaje recibido en bruto: {data}")
                mensaje = json.loads(data.decode('utf-8'))

                id_sensor = mensaje['id']
                valor = mensaje['valor']
                timestamp = mensaje['timestamp']

                with lock:
                    print("[...] Escribiendo en CSV...")
                    with open(archivo_csv, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([id_sensor, valor, timestamp])
                    print("[✔] Datos escritos correctamente")

                print(f"[DATA] ID={id_sensor}, Valor={valor}, Timestamp={timestamp}")
                conn.sendall(b'Datos recibidos y guardados correctamente')

            except (json.JSONDecodeError, KeyError) as e:
                print(f"[ERROR] Error al procesar mensaje: {e}")
                conn.sendall(b'Datos recibidos con errores. No se han guardado.')

    print(f"[-] Conexión cerrada con {addr}")

def validar_archivo_csv(archivo_csv):
    if not os.path.exists(archivo_csv):
        print("[i] CSV no existe. Creando...")
        with open(archivo_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Valor', 'Timestamp'])

def iniciar_servidor(host='localhost', port=5000, archivo_csv='datos_sensores.csv'):
    validar_archivo_csv(archivo_csv)
    
    lock = threading.Lock()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"[SERVIDOR] Escuchando en {host}:{port}")
        
        while True:
            conn, addr = server_socket.accept()
            print(f"[!] Nueva conexión entrante desde {addr}")
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr, lock, archivo_csv))
            hilo.start()

if __name__ == "__main__":
    iniciar_servidor()
