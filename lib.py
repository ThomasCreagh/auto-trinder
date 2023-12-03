from PIL import Image, ImageDraw, ImageFont
from pilmoji import Pilmoji
import textwrap

class TrinderImage:
    def __init__(self, text, background_image_path,
                 font_file_path, file_save_name):
        image = Image.open(background_image_path)
        self.IMAGE_HEIGTH, self.IMAGE_WIDTH = image.size
        self.TEXT_LENGTH = len(text)

        self.MAX_TEXTBOX_HEIGTH = self.IMAGE_HEIGTH//1.5
        self.MAX_TEXTBOX_WIDTH = self.IMAGE_WIDTH//1.2
        self.MAX_FONT_SIZE = 200
        self.TEXT_PADDING = 6

        self.font_size = self.get_font_size()
        self.word_wrap = self.compute_word_wrap() 

        self.generate_image(text, file_save_name,
                            background_image_path, font_file_path)

    def get_font_size(self):
        font_size = self.MAX_FONT_SIZE
        padding_length = ((self.compute_number_of_lines(font_size)-1) *
                          self.TEXT_PADDING)
        paragraph_heigth = self.compute_textbox_heigth(font_size)
        while (paragraph_heigth * 1.3) > self.MAX_TEXTBOX_HEIGTH:
            font_size -= 1
            paragraph_heigth = self.compute_textbox_heigth(font_size)
        return font_size

    def get_start_heigth(self):
        heigth_middle = self.MAX_TEXTBOX_HEIGTH//2
        half_number_of_lines = self.compute_number_of_lines(self.font_size)//2
        heigth_above_middle = (((half_number_of_lines) * self.font_size) +
                               ((half_number_of_lines-1) * self.font_size)) 
        # return heigth_middle - heigth_above_middle + self.font_size + self.TEXT_PADDING
        # return heigth_middle - self.font_size
        return ((self.IMAGE_HEIGTH//2) - self.font_size) - (self.compute_textbox_heigth(self.font_size)//2) * 1.3

    def compute_textbox_heigth(self, font_size):
        return self.compute_number_of_lines(font_size) * font_size

    def compute_word_wrap(self):
        return int((self.TEXT_LENGTH + 0.5) // self.compute_number_of_lines(self.font_size))

    def compute_number_of_lines(self, font_size):
        out = ((self.TEXT_LENGTH * font_size)+0.5)//self.MAX_TEXTBOX_WIDTH
        return out if out >= 1 else 1

    def generate_image(self, text, file_save_name,
                       background_image_path, font_file_path):
        # paragraph = textwrap.wrap(text, width=self.word_wrap)
        paragraph = textwrap.wrap(text, width=int(self.word_wrap))
        im = Image.open(background_image_path) # data/background.jpeg
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype(font_file_path, self.font_size) # data/Arial.ttf

        current_heigth = self.get_start_heigth()
        font_heigth = self.font_size
        for line in paragraph:
            line_width = draw.textlength(line, font=font)
            # draw.text(((self.IMAGE_WIDTH - line_width)//2, current_heigth), line, font=font)
            with Pilmoji(im) as pilmoji:
                pilmoji.text((round((self.IMAGE_WIDTH - line_width)//2), round(current_heigth)), line, font=font)
            current_heigth += font_heigth + self.TEXT_PADDING

        im.save(file_save_name)       
