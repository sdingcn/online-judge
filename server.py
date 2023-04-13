from wsgiref.simple_server import make_server, WSGIServer
from urllib.parse import parse_qs
from socketserver import ThreadingMixIn
import checker
import datetime

def application(environ, start_response):
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    if path == '/' and method == 'POST':
        data = parse_qs(
            environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode(),
            keep_blank_values = True)
        name = data['name'][0]
        code = data['code'][0]
        result = checker.check(code)
        print(f'Date and Time: {str(datetime.datetime.now())}, Name: {name}, Verdict: {result[0]}')
        with open('pages/result.html', 'r') as f:
            response = f.read().format(name, *result).encode()
        status = '200 OK'
    elif path == '/' and method == 'GET':
        with open('pages/submission.html', 'r') as f:
            response = f.read().encode()
        status = '200 OK'
    else:
        response = 'Page Not Found'.encode()
        status = '404 Not Found'
    headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response)))
    ]
    start_response(status, headers)
    return [response]

class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    pass

if __name__ == '__main__':
    make_server('localhost', 8008, application, ThreadingWSGIServer).serve_forever()
