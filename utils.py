import base64
from dataclasses import dataclass
from datetime import datetime
from PIL import Image
from rembg import new_session
import io
import os
import psutil

SESSION_LOG = "./Log/session_creation.txt"
LOG = ".Log/log_file.log"


def load_model(name: str):
    _Model_PATH = "model/u2net.onnx"
    _Model_PATH = _Model_PATH.split("/")[-1]
    _Model_PATH = _Model_PATH.split(".")[0]
    if name == _Model_PATH:
        session = new_session(model_name=_Model_PATH)

        # for testing sessions Logs session creation
        pid = os.getpid()
        mem = psutil.Process(pid).memory_info().rss
        with open(SESSION_LOG, "w") as log:
            log.write(f"Process ID:{pid}, Memory:{mem} SESSION LOADED\n")
    else:
        raise RuntimeError(f"Model {name} not found")

    return session


def create_log(message: str, process: str):
    log_line = f"[{datetime.now()}; Process:{process}] := {message} \n"
    with open(LOG, "a") as log:
        log.write(log_line)


def make_base64(file_path: str) -> str:
    with open(file_path, "rb") as file_bytes:
        output = base64.b64encode(file_bytes.read()).decode()
    return output


def base64_to_image(base64_string: str) -> Image.Image:
    if "," in base64_string:
        base64_string = base64_string.split(",")[1]

    img_data = base64.b64decode(base64_string)
    img_buffer = io.BytesIO(img_data)

    image = Image.open(img_buffer)
    return image


@dataclass
class Response:
    request_id: str
    success: bool
    data: dict
    error_message: str


@dataclass
class Request:
    request_id: str
    data: str
