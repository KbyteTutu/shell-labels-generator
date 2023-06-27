#!/usr/bin/python
# -*- coding: utf-8 -*-
# @ 南无阿弥陀佛，不要有太多bug……
# @ Author: tukechao
# @ Date: 2023-06-27 22:05:45
# @ LastEditors: tukechao
# @ LastEditTime: 2023-06-27 23:43:35
# @ FilePath: /shell-labels-generator/shell_label_gen.py
# @ description: Main function

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageDraw2 import Draw

FONT_PATH = "fonts/sarasa-mono-sc-nerd-regular.ttf"


class ShellLabelGenerator(object):
    def __init__(self):
        pass

    def input_label_framework(self):
        d = {"name": {"value": "断了的牛角凤凰螺", "p1": (5, 5), "p2": (20, 20), "font": "aaa"}}
        return d

    def input_excel_data(self):
        pass

    def generate_picture(self):
        text = "名称:断了的牛角凤凰螺"

        bg = Image.open("default.png")
        draw = ImageDraw.Draw(bg)

        font = self.gen_proper_font((5, 5), (200, 200), draw, FONT_PATH, text)
        if not font:
            raise RuntimeError("Too small for the text")

        draw.text((5, 5), text, font=font, fill="black")
        bg.save("1.png")

    def gen_proper_font(self, p1: tuple, p2: tuple, draw: Draw, font_path: str, text: str) -> int:
        """
        :description: Generate the proper font for the given text, auto resize the font size.
        :param self :
        :param p1 tuple: the position of text left top corner, the anchor.
        :param p2 tuple: the position of text right bottom corner.
        :param draw Draw: the draw object.
        :param font_path str: the font file.
        :param text str: the input text.
        :return: The font object.
        """
        real_width = p2[1] - p1[1]
        real_height = p2[0] - p1[0]
        for x in range(100, 0, -1):
            font = ImageFont.truetype(font_path, x, encoding="utf-8")
            l, t, r, b = draw.textbbox(p1, text, font=font)
            f_width = r - l
            f_height = b - t
            if f_width <= real_width and f_height <= real_height:
                return font
        return None


if __name__ == "__main__":
    ins = ShellLabelGenerator()
    ins.generate_picture()
