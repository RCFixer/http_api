import unittest
import json

import http_api


class HttpApiTests(unittest.TestCase):
    def test_parse_request(self):
        self.assertEqual(http_api.parse_request('GET /234'), (('GET', '234')))
        self.assertEqual(http_api.parse_request(''), (('', 'invalid request')))
        self.assertEqual(http_api.parse_request('POST /123'),
                         (('POST', '123')))
        self.assertEqual(http_api.parse_request('PUT /0'), (('PUT', '0')))
        self.assertEqual(http_api.parse_request('DELETE /sdf'),
                         (('DELETE', 'sdf')))

    def test_generate_headers(self):
        self.assertEqual(http_api.generate_headers('GET'),
                         ('HTTP/1.1 200 OK\n\n', 200))
        self.assertEqual(http_api.generate_headers('POST'),
                         ('HTTP/1.1 405 Method not allowed\n\n', 405))
        self.assertEqual(http_api.generate_headers('PUT'),
                         ('HTTP/1.1 405 Method not allowed\n\n', 405))
        self.assertEqual(http_api.generate_headers('DELETE'),
                         ('HTTP/1.1 405 Method not allowed\n\n', 405))

    def test_generate_content(self):
        self.assertEqual(http_api.generate_content(405, 12, 30),
                         "<error>method not allowed</error>")
        self.assertEqual(
            http_api.generate_content(200, 12, 60),
            json.dumps({
                'ccy': 'USD',
                'requested_value': 12,
                'base_ccy': 'RUR',
                'value': 720.0
            }))
        self.assertEqual(
            http_api.generate_content(200, 240, 63),
            json.dumps({
                'ccy': 'USD',
                'requested_value': 240,
                'base_ccy': 'RUR',
                'value': 15120.0
            }))
        self.assertEqual(
            http_api.generate_content(200, 135, 63.35),
            json.dumps({
                'ccy': 'USD',
                'requested_value': 135,
                'base_ccy': 'RUR',
                'value': 8552.25
            }))
        self.assertEqual(
            http_api.generate_content(200, 0, 63.35),
            json.dumps({
                'ccy': 'USD',
                'requested_value': 0,
                'base_ccy': 'RUR',
                'value': 0.0
            }))
        self.assertEqual(
            http_api.generate_content(200, 1, -63),
            json.dumps({
                'ccy': 'USD',
                'requested_value': 1,
                'base_ccy': 'RUR',
                'value': -63.0
            }))
        self.assertEqual(http_api.generate_content(200, 12, 'error'),
                         "<error>no access to currencies website</error>")
        self.assertEqual(http_api.generate_content(200, 'error', 30),
                         "<error>invalid request</error>")
