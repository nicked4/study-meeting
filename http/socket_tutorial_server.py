import socket

correct_res = '''HTTP/1.1 200 OK

Hello, world!
'''

# IP: IPv4
# Type: TCP
# Port: 8000
# Max Connections: 5

# 上記の設定でソケットを準備する
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 8000))
    sock.listen(5)

    # serving
    while True:
        try:
            (conn, addr) = sock.accept()
            with conn:
                # client からの connect でキックされる
                name = conn.recv(2**32).decode('utf-8')
                print('Connected by' + str(addr))
                print(f'Client name: {name}')
                conn.send(f'Hello, {name}!'.encode('utf-8'))
        except KeyboardInterrupt:
            print('\nStop Serving!')
            break
