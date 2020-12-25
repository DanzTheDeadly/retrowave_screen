#!/usr/bin/env python3
from samplebase import SampleBase
import time


class Test (SampleBase):
    def run(self):
        with open('64x32.pbm') as file:
            pbm = file.read()
        lines = pbm.split('\n')
        size = tuple(map(int, lines[2].split()))
        image = ''.join(lines[3:])

        for i in range(len(image)):
            x = i % size[0]
            y = i // size[0]
            if image[i] == 0:
                self.matrix.SetPixel(x, y, 127, 0 ,0)
        time.sleep(5)

# Main function
if __name__ == "__main__":
    test = Test()
    if (not test.process()):
        test.print_help()
