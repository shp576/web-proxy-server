import socket
import sys
import _thread
import traceback
import ssl
import tkinter as tk
from tkinter import simpledialog

listen_port = 0
max_conn = 10000
buffer_size = 10000

def main():
    global listen_port
    try:
        listen_port = simpledialog.askinteger("Input", "Enter a listening port:")
    except KeyboardInterrupt:
        sys.exit(0)

    initialize_socket()

    root = tk.Tk()
    root.title("Proxy Server GUI")
    
    start_button = tk.Button(root, text="Start Server", command=start_server)
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="Stop Server", command=root.destroy)
    stop_button.pack(pady=10)

    root.mainloop()

def initialize_socket():
    global s
    try:
        global listen_port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("", listen_port))
        s.listen(max_conn)
        print("[*] Initializing socket. Done.")
        print("[*] Socket binded successfully...")
        print("[*] Server started successfully [{}]".format(listen_port))
    except Exception as e:
        print(e)
        sys.exit(2)

def start_server():
    _thread.start_new_thread(accept_connections, ())

def accept_connections():
    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(buffer_size)
            _thread.start_new_thread(conn_string, (conn, data, addr))
        except KeyboardInterrupt:
            s.close()
            print("\n[*] Shutting down...")
            sys.exit(1)
    s.close()

def conn_string(conn, data, addr):
    try:
        print(addr)
        first_line = data.decode('latin-1').split("\n")[0]
        print(first_line)
        url = first_line.split(" ")[1]

        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos + 3):]

        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int(temp[(port_pos + 1):][:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        print(webserver)
        proxy_server(webserver, port, conn, data, addr)
    except Exception as e:
        print(e)
        traceback.print_exc()

def proxy_server(webserver, port, conn, data, addr):
    print("{} {} {} {}".format(webserver, port, conn, addr))
    try:
        s_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_proxy.connect((webserver, port))
        s_proxy.send(data)
        while 1:
            reply = s_proxy.recv(buffer_size)

            if len(reply) > 0:
                conn.sendall(reply)
                print("[*] Request sent: {} > {}".format(addr[0], webserver))
            else:
                break

        s_proxy.close()
        conn.close()

    except Exception as e:
        print(e)
        traceback.print_exc()
        s_proxy.close()
        conn.close()
        sys.exit(1)

if _name_ == "_main_":
    main()
