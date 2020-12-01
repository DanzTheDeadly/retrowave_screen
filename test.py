#!/usr/bin/env python3
import time
import sys
sys.path.append('./lib/rpi-rgb-led-matrix/bindings/python')
sys.path.append('./images')
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import cnf

if len(sys.argv) < 2:
    sys.exit("Require an image argument")
else:
    image_file = sys.argv[1]

image = Image.open(image_file)

# Configuration for the matrix
options = RGBMatrixOptions()
options.cols = cnf.LED_COLS
options.rows = cnf.LED_ROWS
options.chain_length = cnf.CHAIN_LENGTH
options.parallel = cnf.PARALLEL
options.gpio_slowdown = cnf.GPIO_SLOWDOWN
options.hardware_mapping = cnf.GPIO_MAPPING

matrix = RGBMatrix(options=options)
matrix.SetImage(image.convert('RGB'))

try:
    print("Press CTRL-C to stop.")
    print(sys.version)
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    sys.exit(0)
