from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
import requests
from selenium import webdriver
import models.wowItem

item_bp = Blueprint('item', __name__)
from PIL import Image, ImageDraw, ImageFont, ImageOps
import textwrap

class ItemPreview:
    def __init__(self, item_name, item_level, item_rarity, item_image_url, item_description = ""):
        self.item_name = item_name
        self.item_level = item_level
        self.item_rarity = item_rarity
        self.item_description = item_description
        self.item_image_url = item_image_url
        
    
    
    def generate_preview(self):
        # Load font
        font_small = ImageFont.truetype("arial.ttf", 20)
        font_medium = ImageFont.truetype("arial.ttf", 30)
        font_large = ImageFont.truetype("arial.ttf", 40)
        # load colors
        fill_epic = (163, 53, 238)
        fill_gold = (255, 209, 0)
        fill_rare = (53, 93, 238)
        
        background = Image.open("static/tooltip.png")
        
        
        #textwrap
        description_text = self.item_description
        description_lines = self.item_description.split('\\n')  

        # Join wrapped lines with newline characters
        num_lines = len(description_lines)
        line_height = font_small.getsize("A")[1] + 2
        desc_height = num_lines * line_height

        # Determine text height and adjust image size
        text_width, text_height = ImageDraw.Draw(Image.new('RGB', (1, 1))).multiline_textsize(self.item_description, font=font_small)
        img_height = max(200, text_height + 150)
        img = Image.new('RGB', (400, img_height + desc_height), color=(30, 30, 30))
        background = background.resize(img.size)
        img.paste(background, (0, 0))
        d = ImageDraw.Draw(img)

        # Draw item name
        d.text((10, 10), self.item_name, font=font_large, fill=fill_epic)

        # Draw item level and rarity
        level_text = f"Item Level: {self.item_level}"
        rarity_text = f"Rarity: {self.item_rarity}"
        d.text((10, 50), level_text, font=font_medium, fill=fill_gold)
        d.text((10, 80), rarity_text, font=font_medium, fill=(255, 255, 255))

        description_lines = self.item_description.split('\\n')  
        y = 140
        for line in description_lines:
            d.text((10, y), line, font=font_small, fill=(255, 255, 255))
            y += font_small.getsize(line)[1] + 5  # Add some extra padding between lines

        

        # Draw item image
        background_mask = Image.open("static/tooltip.png")
        background_mask = background_mask.resize((80,80))
        item_image = Image.open(requests.get(self.item_image_url, stream=True).raw)
        item_image = item_image.resize((80, 80))
        
        border_size = 5
        border_color = (0, 0, 0)
        border_image = ImageOps.expand(item_image, border=border_size, fill=border_color)
        # Resize the background_mask to the same size as item_image
        mask = background_mask.resize(item_image.size)

        # Apply the mask to item_image
        item_image.putalpha(mask.split()[3])
        default_image = Image.open("static/default.png")
        
        img.paste(border_image, (300, 10))

        return img
    

@item_bp.route('/api/item', methods=['GET'])
def item_preview():
    item_name = request.args.get('name', 'Item Name')
    item_level = request.args.get('level', '1')
    item_rarity = request.args.get('rarity', 'Common')
    item_description = request.args.get('description', '')
    item_image_url = request.args.get('image', 'https://via.placeholder.com/150')

    # Generate the item preview image
    item_preview = ItemPreview(item_name, item_level, item_rarity, item_image_url, item_description)
    img = item_preview.generate_preview()

    # Save the image to a bytes buffer
    img_buffer = BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)

    # Return the image as a file
    return send_file(img_buffer, mimetype='image/png')

    
@item_bp.route('/render_html', methods=['GET'])
def render_html():
    # Get the URL of the HTML file
    url = request.args.get('url')

    # Start a headless browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    #options.add_argument("window-size=390,230")

    driver = webdriver.Chrome(options=options)

    # Load the HTML file and take a screenshot of it
    driver.get(url)
    png = driver.get_screenshot_as_png()

    # Close the browser
    driver.quit()

    # Convert the PNG image to BytesIO object
    img = BytesIO(png)

    # Return the image as the response
    return send_file(img, mimetype='image/png')