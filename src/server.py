#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image
import io


class MatrixRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.server.image.save(self.wfile, format='png')

    def do_POST(self):
        request_content = self.rfile.read(int(self.headers['Content-Length']))
        img_buffer = io.BytesIO()
        img_buffer.write(request_content)
        self.server.image = Image.open(img_buffer).convert('RGB')
        self.server.matrix.SetImage(self.server.image)
        self.send_response(200)
        self.end_headers()


class MatrixController(HTTPServer):
    def __init__(self, config=None, test_mode=False):
        self.matrix_config = config['MATRIX']
        self.server_config = config['SERVER']
        #
        if test_mode:
            from test.dummy_matrix import RGBMatrix, RGBMatrixOptions
        else:
            import sys
            sys.path.append('../lib/rpi-rgb-led-matrix/bindings/python')
            sys.path.append('../images')
            from rgbmatrix import RGBMatrix, RGBMatrixOptions
        self.matrix_opts = RGBMatrixOptions()
        self.matrix_opts.cols = self.matrix_config['LED_COLS']
        self.matrix_opts.rows = self.matrix_config['LED_ROWS']
        self.matrix_opts.chain_length = self.matrix_config['CHAIN_LENGTH']
        self.matrix_opts.parallel = self.matrix_config['PARALLEL']
        self.matrix_opts.gpio_slowdown = self.matrix_config['GPIO_SLOWDOWN']
        self.matrix_opts.hardware_mapping = self.matrix_config['GPIO_MAPPING']
        self.matrix = RGBMatrix(options=self.matrix_opts)
        # set default image when starting
        self.image = Image.open(config['DEFAULT_IMG'])
        self.matrix.SetImage(self.image)
        #
        super().__init__((self.server_config['HOST'], self.server_config['PORT']), MatrixRequestHandler)

    def run(self):
        self.serve_forever()
