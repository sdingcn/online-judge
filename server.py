from wsgiref.simple_server import make_server, WSGIServer
from urllib.parse import parse_qs
from socketserver import ThreadingMixIn
import problem
import datetime
import threading
import time
import re
import sys

L = threading.Lock()

def log(timestamp: str, name: str, code: str, score: str, details: str) -> None:
    underscored_name = re.sub(r'\s+', '_', name)
    prefix = f'logs/{timestamp}-{underscored_name}'
    with open(prefix + '.code', 'w') as f:
        f.write(code)
    with open(prefix + '.result', 'w') as f:
        f.write(f'score={score},details={details}')

def application(environ, start_response):
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    if path == '/' and method == 'POST':
        data = parse_qs(
            environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode(),
            keep_blank_values = True)
        timestamp = str(time.time())
        name = data['name'][0]
        code = data['code'][0]
        score, details = problem.judge(code)
        with L:
            log(timestamp, name, code, score, details)
        with open('pages/result.html', 'r') as f:
            response = f.read().format(name, score, details).encode()
        status = '200 OK'
    elif path == '/' and method == 'GET':
        with open('pages/submission.html', 'r') as f:
            response = f.read().replace('{}', problem.describe()).encode()
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
    try:
        if len(sys.argv) == 1:
            host = 'localhost'
            port = 8008
        elif len(sys.argv) == 3:
            host = sys.argv[1]
            port = int(sys.argv[2])
        else:
            sys.exit(f'Unrecognized number of command line arguments.\nUsage: python3 {sys.argv[0]} [host="localhost"] [port=8008]')
        print(f'Starting server on {host}:{port}.')
        make_server(host, port, application, ThreadingWSGIServer).serve_forever()
    except KeyboardInterrupt:
        print('Server stopped.')
        sys.exit(0)
