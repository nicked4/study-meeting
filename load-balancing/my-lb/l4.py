# TODO:
import socket


def main():
    print('main')
    with socket.socket(socket.AF_PACKET, socket.SOCK_RAW) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 8000))
        sock.listen(5)


if __name__ == '__main__':
    main()
