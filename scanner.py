import sys, socket, time, concurrent.futures

def scan_port(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        if result == 0:
            return port
        s.close()
    except KeyboardInterrupt:
        print("\nExiting program.")
        sys.exit()
    except socket.error:
        print("Couldn't connect to server.")
        sys.exit()

def scan_ports(ip, port_range):
    open_ports = []
    start_port, end_port = map(int, port_range.split('-'))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        port_tasks = {executor.submit(scan_port, ip, port): port for port in range(start_port, end_port + 1)}
        
        for task in concurrent.futures.as_completed(port_tasks):
            port = port_tasks[task]
            result = task.result()
            if result is not None:
                open_ports.append(result)
    
    return open_ports

def save_results(ip, open_ports):
    if open_ports:
        with open("results.txt", "w") as file:
            file.write(f"Open ports for {ip}:\n")
            for port in open_ports:
                file.write(f"Port {port} is open\n")
        print(f"Scan completed. Results saved to results.txt")
    else:
        print("No open ports found.")

def main():
    if len(sys.argv) != 3:
        print("Usage: scanner.py {ip} {port_range}")
        sys.exit(1)

    ip = sys.argv[1]
    port_range = sys.argv[2]

    start_time = time.time()
    
    open_ports = scan_ports(ip, port_range)
    save_results(ip, open_ports)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Scan completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()