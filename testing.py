import base64
from io import BytesIO
import time
from PIL import Image

import requests

LOG_FILE = ''
IMAGE = './Resources/images.jpeg'

def test():
    time.sleep(2)
    with open(IMAGE, 'rb') as image:
        encoded_image = base64.b64encode(image.read()).decode()
    payload = {
        'request_id': 'something something',
        'data': encoded_image
    }
    response = requests.request(method="POST", url='http://127.0.0.1:8000/background_remove/', json= payload)
    encoded_output = response.json().get("data")
    encoded_output = base64.b64decode(encoded_output)
    output_image = Image.open(BytesIO(encoded_output))
    output_image.save('./Resources/result.png', format='png')

if __name__ == "__main__":
    test()
