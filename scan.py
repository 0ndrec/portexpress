import socket
import threading
import subprocess
from queue import Queue
import ipaddress
import sys


def validate_args()-> dict:
    try:
        ip = sys.argv[1]
        ipaddress.ip_address(ip)
    except ValueError:
        print("Invalid IP address")
        sys.exit(1)
    return ip


TARGET_IP = validate_args()
START_PORT = 1
END_PORT = 26670 # To max 65535
PORT_SCAN_THREADS = 16

open_ports = []
port_queue = Queue()


def curl_cmd(target: str, ports: list, timeout: int) -> dict:

    _dict = {}
    for port in ports:
        try:
            response_code = subprocess.check_output(['curl', '-s', '-m', str(timeout), '-w', '%{http_code}', '-o', '/dev/null', f'{target}:{port}'])
            _dict[port] = int(response_code)
        except subprocess.CalledProcessError:
            pass
    return _dict



def scan_port(port) -> list:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((TARGET_IP, port))
            if result == 0:
                print(f" - Found open port: {port}")
                open_ports.append(port)
            return open_ports
    except Exception:
        pass


def port_threader():
    while not port_queue.empty():
        port = port_queue.get()
        try:
            scan_port(port)
            port_queue.task_done()
        except Exception:
            print(f"Error scanning port {port}")
        monitor_progress(completed=port_queue.qsize(), total=END_PORT - START_PORT + 1)


def monitor_progress(completed, total, bar_length=50):
    progress = (completed / total) * 100
    notcompleted = total - completed
    filled_length = int(round(bar_length * progress / 100))
    bar = '-' * (bar_length - filled_length) + '#' * filled_length
    print(f"\rProgress: [{bar}] {notcompleted}/{total} completed ({100-progress:.2f}%)", end="")



def main():
    # Сканирование портов
    print("Scanning ports...\n")
    for port in range(START_PORT, END_PORT + 1):
        port_queue.put(port)
    
    port_threads = []
    for _ in range(PORT_SCAN_THREADS):
        t = threading.Thread(target=port_threader)
        t.daemon = True
        t.start()
        port_threads.append(t)
    
    port_queue.join()
    
    print("\n")
    if not open_ports:
        print("No open ports found.")
        return
    
    print("\nList of open ports: ", open_ports)

    print("\nScanning web services on ports with curl...\n")
    
    resp_codes = {
        200: 'OK',
        301: 'Moved Permanently',
        302: 'Found',
        304: 'Not Modified',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        500: 'Internal Server Error',
        502: 'Bad Gateway',
        503: 'Service Unavailable'
    }

    curl_results = curl_cmd(TARGET_IP, open_ports, 2)
    
    for port, response in curl_results.items():
        description = resp_codes.get(response, "Unknown Response")
        print(f"Port {port}: {response} - {description}")
    
if __name__ == "__main__":
    main()

