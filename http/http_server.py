import socket

class RequestParser():
    def __init__(self, req):
        self.http_version = None
        self.method = None
        self.host = None
        self.path = None
        self.query = None
        self.headers = None
        self.body = None
        self.parse_req(req)

    def parse_req(self, req):
        lines = req.splitlines()
        request_line = lines[0]
        separate_index = lines.index('')

        route = request_line.split()[1]
        raw_headers = lines[1:separate_index]
        headers = {
            h.split(':', 1)[0].strip().lower(): h.split(':', 1)[1].strip().lower()
            for h in raw_headers
        }

        query = route.split('?')[1] if (len(route.split('?')) == 2) else ''
        mapped_query = {} if query == '' else {
            s.split('=')[0]: s.split('=')[1]
            for s in query.split('&')
        }

        self.http_version = request_line.split()[2]
        self.method = request_line.split()[0].upper()
        self.host = headers.pop('host')
        self.path = request_line.split()[1].split('?')[0]
        self.query = mapped_query
        self.headers = headers
        self.body = '\n'.join(lines[separate_index + 1:])


def validate_method(method):
    def wrapper(f):
        def _wrapper(req, conn):
            if req.method != method:
                method_not_allowed(req, conn)
                return
            f(req, conn)
        return _wrapper
    return wrapper


def method_not_allowed(req, conn):
    request_line = 'HTTP/1.1 405 method not allowed'
    body = f'{req.path} does not allow {req.method} method'
    conn.send('\n'.join([request_line, '', body]).encode('utf-8'))


@validate_method('GET')
def get(req, conn):
    request_line = 'HTTP/1.1 200 ok'
    body = 'Hello, world!'
    conn.send('\n'.join([request_line, '', body]).encode('utf-8'))


@validate_method('GET')
def greet(req, conn):
    request_line = 'HTTP/1.1 200 ok'
    name = req.path.strip('/').split('/')[1]
    conn.send('\n'.join([request_line, '', f'Hello, {name}!']).encode('utf-8'))


@validate_method('GET')
def redirect(req, conn):
    request_line = 'HTTP/1.1 301 moved parmanently'
    headers = { 'Location': '/' }
    conn.send('\n'.join([
        request_line,
        '\n'.join([ f'{k}: {v}' for k, v in headers.items()]),
        '',
        'redirect to /',
    ]).encode('utf-8'))


@validate_method('GET')
def redirect_spy(req, conn):
    request_line = 'HTTP/1.1 200 moved parmanently'
    headers = { 'Location': '/' }
    conn.send('\n'.join([
        request_line,
        '\n'.join([ f'{k}: {v}' for k, v in headers.items()]),
        '',
        'redirect to /',
    ]).encode('utf-8'))


@validate_method('GET')
def internal_server_error(req, conn):
    request_line = 'HTTP/1.1 500 internal server error'
    conn.send('\n'.join([request_line, '', 'ERROR!!!!!',]).encode('utf-8'))


@validate_method('GET')
def html(req, conn):
    request_line = 'HTTP/1.1 200 ok'
    with open('static/hello_world.html') as f:
        raw_html = f.read()
        conn.send('\n'.join([request_line, '', raw_html,]).encode('utf-8'))


def not_found(req, conn):
    request_line = 'HTTP/1.1 404 not found'
    body = f'Not Found: {req.method} {req.path}'
    conn.send('\n'.join([request_line, '', body]).encode('utf-8'))


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 8000))
        sock.listen(5)

        print('Start Serving!')
        while True:
            try:
                (conn, _) = sock.accept()
                with conn:
                    r = conn.recv(2**32).decode('utf-8')
                    req = RequestParser(r)

                    if req.path == '/':
                        get(req, conn)
                    elif req.path.startswith('/greet'):
                        greet(req, conn)
                    elif req.path == '/redirect':
                        redirect(req, conn)
                    elif req.path == '/redirect/spy':
                        redirect_spy(req, conn)
                    elif req.path == '/error':
                        internal_server_error(req, conn)
                    elif req.path == '/html':
                        html(req, conn)
                    else:
                        not_found(req, conn)
            except KeyboardInterrupt:
                print('\nStop Serving!')
                break
