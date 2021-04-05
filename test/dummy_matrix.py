from PIL import Image


class RGBMatrixOptions:
    def __init__(self):
        self.cols = None
        self.rows = None
        self.chain_length = None
        self.parallel = None
        self.gpio_slowdown = None
        self.hardware_mapping = None


class RGBMatrix:
    def __init__(self, options: RGBMatrixOptions):
        self.options = options
        self.image = None
        print('Matrix created')

    def SetImage(self, img):
        self.image = img
        print('Image set')

    def SetPixel(self, x, y, R, G, B):
        print('Set pixel at x={x} y={y} to {R}-{G}-{B}'.format(x=x, y=y, R=R, G=G, B=B))

    def get_image(self):
        return bytes(self.image)
