import socket

def main():
    proxy_host = "172.16.7.164"  # Replace with the actual IP address or hostname of the proxy server
    proxy_port = 5050  # Replace with the actual port number of the proxy server

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((proxy_host, proxy_port))

        # Sending a simple HTTP GET request as an example
        request = "GET / HTTP/1.1\r\n Host: www.example.com\r\n\r\n"
        s.sendall(request.encode('utf-8'))

        # Receiving and printing the response
        response = s.recv(4096)
        print(response.decode('utf-8'))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    main()
