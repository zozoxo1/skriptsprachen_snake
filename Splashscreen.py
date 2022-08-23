import sys

sys.path.append('/home/pi/rpi_rgb_led_matrix/bindings/python/samples')
from samplebase import SampleBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from enums.GameStatus import GameStatus

import threading
import time

class Splashscreen(SampleBase):

    def __init__(self, *args, **kwargs):
        super(Splashscreen, self).__init__(self, *args, **kwargs)
        self._running = True
        self.status = GameStatus.WAITING_FOR_NEXT_PLAYER

    def terminate(self):
        self._running = False

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()

        font = graphics.Font()
        font.LoadFont("/home/pi/rpi_rgb_led_matrix/fonts/6x12.bdf")
        textColor = graphics.Color(255, 255, 0)
        pos = offset_canvas.width
        my_text = "tetris.informatik.fh-swf.de"

        while self._running and self.status == GameStatus.WAITING_FOR_NEXT_PLAYER:

            offset_canvas.Clear()

            graphics.DrawText(offset_canvas, font, 18, 10, textColor, "Snake")
            graphics.DrawText(offset_canvas, font, 13, 20, textColor, "spielen")
            graphics.DrawText(offset_canvas, font, 18, 30, textColor, "unter")
            graphics.DrawText(offset_canvas, font, 28, 40, textColor, "\/")

            for i in range(2, self.matrix.width-2):
                offset_canvas.SetPixel(
                    i,
                    48,
                    255,
                    255,
                    255
                )

            len = graphics.DrawText(offset_canvas, font, pos, 60, textColor, my_text)
            pos -= 1
            if (pos + len < 0):
                pos = offset_canvas.width

            time.sleep(0.03)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

        offset_canvas.Clear()