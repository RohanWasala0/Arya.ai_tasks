import asyncio
import base64
import uuid
from io import BytesIO
import time
from PIL import Image

import requests

from ImageHologramSign import ImageHologramSign
from utils import Request, make_base64

LOG_FILE = './temp/session_creation.txt'
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
    print(response.headers)
    encoded_output = response.json().get("data")
    encoded_output = base64.b64decode(encoded_output)
    output_image = Image.open(BytesIO(encoded_output))
    output_image.save('./Resources/result.png', format='png')
    print_resp = response.json()
    print_resp["data"] = './Resources/result.png'
    print(print_resp)

def test_with_workers(no_of_workers: int):
    # if os.path.exists(LOG_FILE):
    #     os.remove(LOG_FILE)

    time.sleep(2)

    # Send 1 request per worker
    with open(IMAGE, 'rb') as image:
        encoded_image = base64.b64encode(image.read()).decode()
    for x in range(no_of_workers):
        payload = {
            'request_id': f"worker {x} request_id",
            'data': encoded_image
        }
        response = requests.request(method="POST", url="http://127.0.0.1:8000/background_remove/", json=payload)
        assert response.status_code == 200

    time.sleep(1)

    # AI generated
    # Read the log
    with open(LOG_FILE) as f:
        lines = f.readlines()

    # There should be 4 unique worker PIDs
    pids = {line.split("ID:")[1].split(",")[0] for line in lines}

    assert len(pids) == 4, f"Expected 4 worker PIDs, got {pids}"

    # Also check that each worker loaded exactly 1 model
    sessions = len(lines)
    assert sessions == 4, f"Expected 4 SESSION loads, got {sessions}"

    # Optional: print memory usage
    print("Worker memory usage info:")
    print("".join(lines))

async def test_task2():

    req_id = str(uuid.uuid4())
    request: Request = Request(
        request_id= req_id,
        data= make_base64('./Resources/Untitled.jpg')
    )

    response = await ImageHologramSign.run(request)
    print(response)

if __name__ == "__main__":
    asyncio.run(test_task2())
