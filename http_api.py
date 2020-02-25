import socket
import json
import xml.etree.ElementTree as ET
import urllib.request
import logging.config

from settings import logger_config

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger')

def get_current_currency():
    opener = urllib.request.build_opener()
    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    try:
        currency = ET.parse(opener.open(url)).find('Valute[@ID="R01235"]').find('Value').text.replace(',','.')
    except:
        logger.debug('no access to currencies website')
        currency = 'error'
    return currency

def parse_request(request):
    parsed = request.split(' ')
    method = parsed[0]
    try:
        rur = parsed[1][1:]
    except IndexError:
        logger.debug(request)
        rur = 'invalid request'
    return (method, rur)

def generate_headers(method):
    if not method == 'GET':
        return ('HTTP/1.1 405 Method not allowed\n\n', 405)
    return ('HTTP/1.1 200 OK\n\n', 200)

def generate_content(code, rur, usd):
    if code == 405:
        return "<error>method not allowed</error>"
    if usd == 'error':
        return "<error>no access to currencies website</error>"
    try:
        result = json.dumps({'ccy': 'USD',
                             'requested_value': rur,
                             'base_ccy': 'RUR',
                             'value': int(rur) * float(usd)})
    except ValueError:
        result = "<error>invalid request</error>"
    return result

def generate_response(request):
    method, rur = parse_request(request)
    headers, code = generate_headers(method)
    usd = get_current_currency()
    body = generate_content(code, rur, usd)
    logger.debug((headers + body).encode())
    return (headers + body).encode()

def run():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0', 5000))
    server_socket.listen()

    while True:
        try:
            client_socket, _ = server_socket.accept()
        except KeyboardInterrupt:
            client_socket.close()
            break
        else:
            request = client_socket.recv(1024)
            logger.debug(request.decode('utf-8'))

            response = generate_response(request.decode('utf-8'))

            client_socket.sendall(response)
            client_socket.close()

if __name__ == '__main__':
    run()