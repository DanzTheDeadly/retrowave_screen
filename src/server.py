#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from PIL import Image
import io
import base64
import cgi


class MatrixRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        img_buffer = io.BytesIO()
        self.server.image.save(img_buffer, format='png')
        img_data = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        with open('src/index.html') as page:
            page_final = page.read().format(img_data).encode('utf-8')
            self.wfile.write(page_final)

    def do_POST(self):
        content_type, pdict = cgi.parse_header(self.headers['content-type'])
        pdict['boundary'] = pdict['boundary'].encode('ascii')
        result = cgi.parse_multipart(self.rfile, pdict)
        image_extracted = b''.join(result['image'])
        img_buffer = io.BytesIO()
        img_buffer.write(image_extracted)
        try:
            self.server.image = Image.open(img_buffer).convert('RGB').resize((192, 96))
            self.server.matrix.SetImage(self.server.image)
        except Image.UnidentifiedImageError:
            self.send_response(400, message='Unknown format')
        else:
            self.do_GET()
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
