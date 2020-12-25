from PIL import Image


class RGBMatrixOptions:
    def __init__(self, **kwargs):
        self.options = kwargs


class RGBMatrix:
    def __init__(self, options: RGBMatrixOptions):
        self.options = options
        self.image = b'0'
        print('Matrix created')

    def SetImage(self, img):
        self.image = img
        print('Image set')

    def SetPixel(self, x, y, R, G, B):
        print('Set pixel at x={x} y={y} to {R}-{G}-{B}'.format(x=x, y=y, R=R, G=G, B=B))

    def get_image(self):
        return self.image