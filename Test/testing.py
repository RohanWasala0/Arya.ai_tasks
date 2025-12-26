import asyncio
import base64
import uuid
import time

import requests

from fastapi.testclient import TestClient
from .main import app

from utils import Request, create_log, make_base64

CLIENT = TestClient(app)


def test_background_remove():
    def single_iteration(iteration: int):
        payload = {
            "request_id": f"test_iteration {iteration}",
            "data": make_base64("./Resources/images.jpeg"),
        }

        start = time.time()
        response = CLIENT.post("/background_remove/", json=payload)
        duration = time.time() - start

        create_log(
            message=f"[{iteration}] Status: {response.status_code}, Time: {duration:.3f}, Header: {response.headers}",
            process="Background Remove",
        )

        assert response.status_code == 200
        assert response.json().get("data"), "No data in response"

        return True

    number_request = 10
    create_log()


def test_with_workers(no_of_workers: int):
    # if os.path.exists(LOG_FILE):
    #     os.remove(LOG_FILE)

    time.sleep(2)

    # Send 1 request per worker
    with open(IMAGE, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode()
    for x in range(no_of_workers):
        payload = {"request_id": f"worker {x} request_id", "data": encoded_image}
        response = requests.request(
            method="POST", url="http://127.0.0.1:8000/background_remove/", json=payload
        )
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
        request_id=req_id, data=make_base64("./Resources/Untitled.jpg")
    )
    payload = {"request_id": req_id, "data": make_base64("./Resources/Untitled.jpg")}

    # response: Response = await ImageHologramSign.run(request)
    response = requests.request(
        method="POST", url="http://127.0.0.1:8000/image_hologram_sign/", json=payload
    )

    # import ast
    # response_data = ast.literal_eval(response.data)
    # print(f"Image Quality Data: {response_data.get('image quality data')}")
    # print(f"Hologram Data: {response_data.get('hologram data')}")
    # response_data.get('signature data')['base64'] = None
    # print(f"Signature Data: {response_data.get('signature data')}")


if __name__ == "__main__":
    asyncio.run(test_task2())
