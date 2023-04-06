from PIL import Image, ImageDraw, ImageFont

class ImageGenerator:
    def __init__(self, text):
        self.text = text

    def generate_image(self):
        img = Image.new('RGB', (400, 200), color = (73, 109, 137))

        d = ImageDraw.Draw(img)
        font = ImageFont.truetype("arial.ttf", 60)
        d.text((50, 50), self.text, fill=(255, 255, 0), font=font)

        return img
