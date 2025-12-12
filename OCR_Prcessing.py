from typing import Dict, List
from PIL import Image, ImageDraw
from random import choice
import json

def process_json(file_path: str) -> List:
    with open(file_path, 'r') as file:
        OCR_result_json = json.load(file)
    print(OCR_result_json.get('analyzeResult').keys())
    words: List = []
    if 'pages' in OCR_result_json.get('analyzeResult').keys():
        pages = OCR_result_json.get('analyzeResult')['pages']
        # print(type(pages)) #list
        # print(len(pages)) #1
        # print(type(pages[0])) #dict
        words = pages[0].get('words')
    return words

def load_as_clean_rgba(path):
    img = Image.open(path).convert("RGBA")

    # flatten the JPEG onto a white background
    clean = Image.new("RGBA", img.size, (255, 255, 255, 255))
    clean.paste(img, mask=img.split()[3] if img.mode == 'RGBA' else None)

    return clean

def draw_polygons(image: Image.Image):
    print(image.getpixel((0, 0)))
    words = process_json('./Resources/story1.json')
    draw = ImageDraw.Draw(image, 'RGBA')
    print(image.mode, draw.mode)
    fill_colors = [(248, 244, 236, 200), (255, 143, 183, 20), (232, 60, 145, 200), (67, 51, 76, 200)]
    for word in words:
        coordinates = word.get('polygon')
        draw.polygon(xy= coordinates, outline='black')
    image.save('./Resources/output_some.png', format='png')

try:
    input_image = load_as_clean_rgba('./Resources/story1.jpg')
    draw_polygons(input_image)
except Exception as e:
    print('Something is wrong', e)

