import sys

sys.path.append('/home/pi/rpi_rgb_led_matrix/bindings/python/samples')
from samplebase import SampleBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions

from Playground import Playground
from enums.PlaygroundTile import PlaygroundTile

class Display(SampleBase):

    def __init__(self, *args, **kwargs):
        super(Display, self).__init__(*args, **kwargs)
        self.playground: Playground = Playground(20, 20)

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        
        while True:
            self.draw(self.playground.getPlaygroundMatrix(), offset_canvas)

    def draw(self, matrix, offset_canvas):
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                # width - height - endwidth - endheight
                color: tuple = (0, 0, 0)

                if matrix[row][col] == PlaygroundTile.VOID:
                    color = (0, 0, 255)
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
                            col * 2 + i,
                            row * 2 + k,
                            int(brightness*color[0]),
                            int(brightness*color[1]), 
                            int(brightness*color[2])
                        )


        offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

"""
if __name__ == '__main__':
    dp = Display()
    dp.process()
"""