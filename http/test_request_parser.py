from http_server import RequestParser


req = '''POST /users/1?q1=test&q2=dummy HTTP/1.1
Host: localhost:8000
Content-Type: Application/json
Content-Length: 111

{"id": 123, "name": "anonymous"}
'''

print('test start')

parsed_req = RequestParser(req)
assert (parsed_req.http_version == 'HTTP/1.1')
assert (parsed_req.method == 'POST')
assert (parsed_req.host == 'localhost:8000')
assert (parsed_req.path == '/users/1')
assert (parsed_req.query == { 'q1': 'test', 'q2': 'dummy' })
assert (parsed_req.headers == {'content-type': 'application/json', 'content-length': '111'})
assert (parsed_req.body == '{"id": 123, "name": "anonymous"}')

print('all test have passed')
