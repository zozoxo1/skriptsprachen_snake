import sys

sys.path.append('/home/pi/rpi_rgb_led_matrix/bindings/python/samples')
from samplebase import SampleBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from Playground import Playground
from enums.PlaygroundTile import PlaygroundTile

import multiprocessing

class Display(SampleBase):

    def __init__(self, *args, **kwargs):
        super(Display, self).__init__(self, *args, **kwargs)
        self.playground = Playground(20, 20)

    def setPlayground(self, playground: Playground):
        self.playground = playground

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        
        while True:
            self.draw(self.playground.getPlaygroundMatrix(), offset_canvas)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

    def draw(self, matrix, offset_canvas):
        offsetX = 11
        offsetY = 7
        #offset_canvas.Clear()
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                # width - height - endwidth - endheight
                color: tuple = (0, 0, 0)

                if matrix[row][col] == PlaygroundTile.VOID:
                    color = (4, 10, 240)
                elif matrix[row][col] == PlaygroundTile.SNAKE:
                    color = (248, 255, 4)
                elif matrix[row][col] == PlaygroundTile.FOOD:
                    color = (255, 4, 21)
                elif matrix[row][col] == PlaygroundTile.TEXT:
                    color = (255, 255, 255)
                elif matrix[row][col] == PlaygroundTile.WALL:
                    color = (255, 255, 255)

                brightness = 1
                for i in range(0, 4):
                    for k in range(0, 4):
                        offset_canvas.SetPixel(
                            col * 2 + i + offsetX,
                            row * 2 + k + offsetY,
                            int(brightness*color[0]),
                            int(brightness*color[1]), 
                            int(brightness*color[2])
                        )

if __name__ == '__main__':
    d = Display()
    pg = Playground(20, 20)
    pg.setTile(5, 5, PlaygroundTile.SNAKE)
    d.setPlayground(pg)
    pg.setTile(2, 2, PlaygroundTile.FOOD)
    d.process()