import socket
import threading

open_ports = []
closed_ports = []
lock = threading.Lock()  # It is used a lock to prevent race conditions

def scan_port(hostname, port):
    try:
        ip = socket.gethostbyname(hostname)
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect((ip, port))
        msg = client.recv(1024)
    except socket.timeout:
        with lock:
            closed_ports.append(port)
        print(f"Port {port} is closed (timeout)")
    except socket.error as e:
        with lock:
            closed_ports.append(port)
        print(f"Port {port} is closed ({e})")
    else:
        with lock:
            open_ports.append(port)
        print(f"Port {port} is open")
        print(msg)
    finally:
        client.close()

def main():
    hostname = input("Enter hostname in format (nepal.com, ac.edu.np): ")
    port_range = input("Enter port range separated by space: ")
    first_port, last_port = map(int, port_range.split())

    threads = []
    for port in range(first_port, last_port + 1):
        thread = threading.Thread(target=scan_port, args=(hostname, port))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    open_ports.sort()
    print(f"The open ports between {first_port} - {last_port} are: ")
    for port in open_ports:
        print(port)
    closed_ports.sort()
    print(f"The closed ports between {first_port} - {last_port} are: ")
    for port in closed_ports:
        print(port)

if __name__ == "__main__":
    main()
