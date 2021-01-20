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
        self.image = bytearray(b'0' * self.options.cols * self.options.chain_length * self.options.rows * self.options.parallel)
        print('Matrix created')

    def SetImage(self, img):
        self.image = img
        print('Image set')

    def SetPixel(self, x, y, R, G, B):
        print('Set pixel at x={x} y={y} to {R}-{G}-{B}'.format(x=x, y=y, R=R, G=G, B=B))

    def get_image(self):
        img = ''
        start = 0
        for counter in range(self.options.cols * self.options.chain_length,
                             len(self.image),
                             self.options.cols * self.options.chain_length):
            img += self.image[start:counter].decode() + '\n'
            start = counter
        return img.encode()
