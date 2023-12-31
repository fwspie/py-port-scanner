import socket
import threading
from queue import Queue

def scan_ports(target, start_port, end_port, num_threads):
    def worker():
        while True:
            port = port_queue.get()
            if port is None:
                break
            if scan_port(port):
                open_ports.append(port)
                print(f"\rScanning port {port}... [OPEN]", end="")
            else:
                print(f"\rScanning port {port}... [CLOSED]", end="")
            port_queue.task_done()

    def scan_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target, port))

        sock.close()

        return result == 0

    port_queue = Queue()
    open_ports = []

    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    # Add a sentinel value for each thread to signal them to exit
    for _ in range(num_threads):
        port_queue.put(None)

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print("\nOpen ports:", " | ".join(map(str, open_ports)))

if __name__ == "__main__":
    target_host = input("Enter target host: ")
    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))
    num_threads = int(input("Enter number of threads: "))

    scan_ports(target_host, start_port, end_port, num_threads)
