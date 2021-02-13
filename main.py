import sys
sys.path.append('../lib/rpi-rgb-led-matrix/bindings/python')
sys.path.append('../images')

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from http.server import BaseHTTPRequestHandler, HTTPServer
from yaml import safe_load
from PIL import Image
import io


class MatrixRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        img_buffer = io.BytesIO()
        img_buffer.write(data)
        img = Image.open(img_buffer).convert('RGB')
        self.server.matrix.SetImage(img)
        self.send_response(200)
        self.end_headers()


class MatrixController(HTTPServer):
    def __init__(self, *args, config=None, **kwargs):
        self.matrix_config = config['MATRIX']
        self.server_config = config['SERVER']
        #
        self.matrix_opts = RGBMatrixOptions()
        self.matrix_opts.cols = self.matrix_config['LED_COLS']
        self.matrix_opts.rows = self.matrix_config['LED_ROWS']
        self.matrix_opts.chain_length = self.matrix_config['CHAIN_LENGTH']
        self.matrix_opts.parallel = self.matrix_config['PARALLEL']
        self.matrix_opts.gpio_slowdown = self.matrix_config['GPIO_SLOWDOWN']
        self.matrix_opts.hardware_mapping = self.matrix_config['GPIO_MAPPING']
        self.matrix = RGBMatrix(options=self.matrix_opts)
        #
        super().__init__((self.server_config['HOST'], self.server_config['PORT']), MatrixRequestHandler)

    def run(self):
        self.serve_forever()


if __name__ == '__main__':
    print('Run')
    with open('conf.yaml') as conf_file:
        config = safe_load(conf_file)
    matrixController = MatrixController(config=config)
    try:
        print('Press CTRL-C to stop.')
        print(sys.version)
        matrixController.run()

    except KeyboardInterrupt:
        sys.exit(0)
