import sys
import socket
import threading

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print(f"failed to listen on {local_host} on port {local_port}")
        print("!! Check for other listening sockets or have proper permissions.")
        sys.exit(0)
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        print(f"received connection from {addr[0]} , {addr[1]} ")
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./TCP_Proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./TCP_Proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5].lower() in ['true', '1', 'yes']
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        remote_buffer = response_handler(remote_buffer)
        if len(remote_buffer):
            print("Sending in bytes to localhost")
            client_socket.send(remote_buffer)
    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print("Received in bytes from localhost")
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("Sent to remote >>>")
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("Received in bytes from remote")
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("<<< sent to localhost")
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[+] no more data closing connections")
            break

def hexdump(src, length=16):
    result = []
    if isinstance(src, bytes):
        digits = 2
    else:
        src = src.encode()
        digits = 2
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = ' '.join([f"{b:0{digits}X}" for b in s])
        text = ''.join([chr(b) if 0x20 <= b < 0x7F else '.' for b in s])
        result.append(f"{i:04X}  {hexa:<{length*(digits+1)}} {text}")
    print('\n'.join(result))

def receive_from(connection):
    buffer = b""
    connection.settimeout(2)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer

def request_handler(buffer):
    return buffer

def response_handler(buffer):
    return buffer

main()
