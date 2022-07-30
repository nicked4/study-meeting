import socket

req = '''GET / HTTP/2
Host: localhost:8000
'''

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('localhost', 8000))
    sock.send('Nike'.encode('utf-8'))
    data = sock.recv(64)
    print(data.decode('utf-8'))
