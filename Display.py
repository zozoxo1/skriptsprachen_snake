import sys

sys.path.append('/home/pi/rpi_rgb_led_matrix/bindings/python/samples')
from samplebase import SampleBase
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

from Playground import Playground
from Player import Player
from enums.PlaygroundTile import PlaygroundTile
from enums.GameStatus import GameStatus

import threading

import numpy as np

class Display(SampleBase):

    def __init__(self, *args, **kwargs):
        super(Display, self).__init__(self, *args, **kwargs)
        self.playground = Playground(20, 20)
        self.player = Player(self.playground)
        self._running = True

    def terminate(self):
        self._running = False

    def setPlayground(self, playground: Playground):
        self.playground = playground

    def setPlayer(self, player: Player):
        self.player = player

    def getPlayground(self):
        matrix = self.playground.getPlaygroundMatrix()

        """out = [None]*len(matrix)
        N = len(matrix)
        M = len(matrix[0])

        for i in range(0, len(matrix)):
            out[i] = matrix[i]

        out = np.rot90(out, 2)"""

        return matrix

    def run(self):
        offset_canvas = self.matrix.CreateFrameCanvas()
        
        while self._running:
            self.draw(offset_canvas)
            offset_canvas = self.matrix.SwapOnVSync(offset_canvas)

    def draw(self, offset_canvas):
        matrix = self.getPlayground()
        offsetX = 32 - (int(len(self.getPlayground())) * 2) / 2
        offsetY = 20
        offset_canvas.Clear()
        font = graphics.Font()
        font.LoadFont("/home/pi/rpi_rgb_led_matrix/fonts/4x6.bdf")
        text_length = len("Score: " + str(self.player.getScore())) * 4
        graphics.DrawText(
            offset_canvas,
            font,
            32 - (int(text_length / 2)), 15,
            graphics.Color(255, 255, 255),
            "Score: " + str(self.player.getScore())
        )

        for row in range(0, len(matrix)):
            for col in range(0, len(matrix[0])):
                # width - height - endwidth - endheight
                color: tuple = (0, 0, 0)
                brightness = 1
                brightness_background = 0.2

                if matrix[row][col] == PlaygroundTile.VOID:
                    color = (
                        56 * brightness_background,
                        65 * brightness_background,
                        242 * brightness_background
                    )
                elif matrix[row][col] == PlaygroundTile.SNAKE:
                    color = (
                        248 * brightness,
                        255 * brightness,
                        4 * brightness
                    )
                elif matrix[row][col] == PlaygroundTile.FOOD:
                    color = (
                        255 * brightness,
                        4 * brightness,
                        21 * brightness
                    )
                elif matrix[row][col] == PlaygroundTile.TEXT:
                    color = (
                        255 * brightness,
                        255 * brightness,
                        255 * brightness
                    )
                elif matrix[row][col] == PlaygroundTile.WALL:
                    color = (
                        255 * brightness,
                        255 * brightness, 
                        255 * brightness
                    )

                for i in range(0, 2):
                    for k in range(0, 2):
                        offset_canvas.SetPixel(
                            col * 2 + k + offsetX,
                            row * 2 + i + offsetY,
                            color[0],
                            color[1], 
                            color[2]
                        )