import socket
import datetime
import json
import threading
import logging
from logging.handlers import RotatingFileHandler
import time
import signal

############################################################
# CONFIGURACIÓN DEL HONEYPOT
############################################################

HOST = "0.0.0.0"
PORT = 22  # Puerto SSH simulado
LOG_FILE = "honeypot_logs.json"
MAX_LOG_SIZE = 5 * 1024  # 5 KB
BACKUP_COUNT = 3
TIMEOUT_MINUTES = 60  # tiempo en minutos para apagado automático


############################################################
# CONFIGURACIÓN DEL LOGGER
############################################################

def configurar_logger():
    """Configura el logger con rotación y salida en JSON."""
    logger = logging.getLogger("HoneypotLogger")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


############################################################
# CLASE PRINCIPAL DEL HONEYPOT
############################################################

class Honeypot:
    def __init__(self, host=HOST, port=PORT, timeout_minutes=TIMEOUT_MINUTES):
        self.host = host
        self.port = port
        self.timeout_seconds = timeout_minutes * 60
        self.connection_count = 0
        self.lock = threading.Lock()
        self.running = True
        self.start_time = time.time()
        self.logger = configurar_logger()

        # Manejo de señales (Ctrl+C o kill)
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)

    ########################################################
    # FUNCIONES DE REGISTRO Y LOGGING
    ########################################################

    def log_connection(self, ip, port):
        """Registra intento de conexión en el log JSON."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "ip": ip,
            "port": port,
            "event": "connection_attempt"
        }
        self.logger.info(json.dumps(log_entry))
        with self.lock:
            self.connection_count += 1
            print(f"[{self.connection_count}] Conexión detectada desde {ip}:{port} a las {timestamp}")

    def log_error(self, error, ip=None, port=None):
        """Registra un error en el log JSON."""
        log_entry = {"error": str(error)}
        if ip:
            log_entry["ip"] = ip
        if port:
            log_entry["port"] = port
        self.logger.error(json.dumps(log_entry))

    ########################################################
    # FUNCIONES DE MANEJO DE CONEXIONES
    ########################################################

    def handle_connection(self, client_socket, client_address):
        """Maneja una conexión entrante (responde y registra)."""
        ip, port = client_address
        self.log_connection(ip, port)
        try:
            client_socket.send(b"Acceso denegado. Este evento ha sido registrado.\n")
        except Exception as e:
            self.log_error(e, ip, port)
        finally:
            client_socket.close()

    ########################################################
    # FUNCIONES DE APAGADO Y SEÑALES
    ########################################################

    def shutdown_handler(self, signum, frame):
        """Maneja la señal de apagado (Ctrl+C o kill)."""
        print(f"\n[!] Honeypot apagado por señal ({signum}).")
        self.running = False

    ########################################################
    # INICIO DEL SERVIDOR HONEYPOT
    ########################################################

    def start(self):
        """Inicia el honeypot y escucha conexiones en el puerto configurado."""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(10)
        server.settimeout(1)  # Evita bloqueo indefinido en accept()

        print(f"[+] Honeypot activo en puerto {self.port}. Esperando conexiones...")

        try:
            while self.running:
                # Apagado automático si no hay actividad en X minutos
                if self.connection_count == 0 and (time.time() - self.start_time) > self.timeout_seconds:
                    print(f"\n[!] No se detectaron intentos en {self.timeout_seconds // 60} minutos. Apagando honeypot...")
                    break
                try:
                    client_socket, client_address = server.accept()
                    thread = threading.Thread(target=self.handle_connection, args=(client_socket, client_address))
                    thread.daemon = True
                    thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    self.log_error(e)
        finally:
            server.close()
            print("[+] Honeypot cerrado correctamente.")


############################################################
# PUNTO DE ENTRADA
############################################################

if __name__ == "__main__":
    honeypot = Honeypot()
    honeypot.start()