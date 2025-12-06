import base64
from dataclasses import dataclass
from typing import Any
from PIL.Image import Image
from rembg import new_session
import os
import psutil

SESSION_LOG = "./temp/session_creation.txt"

def load_model(name:str):
    _Model_PATH = 'model/u2net.onnx'
    _Model_PATH = _Model_PATH.split("/")[-1]
    _Model_PATH = _Model_PATH.split(".")[0]
    if name == _Model_PATH:
        session = new_session(model_name=_Model_PATH)

        #for testing sessions Logs session creation 
        pid = os.getpid()
        mem = psutil.Process(pid).memory_info().rss
        with open(SESSION_LOG, "w") as log:
            log.write(f"Process ID:{pid}, Memory:{mem} SESSION LOADED\n")
    else:
        raise RuntimeError(
            f"Model {name} not found"
        )

    return session

def make_base64(file_path: str) -> str:
    with open(file_path, 'rb') as file_bytes:
        output = base64.b64encode(file_bytes.read()).decode()
    return output

@dataclass
class Response:
    request_id: str
    success: bool
    data: str | Image
    error_message: str

@dataclass
class Request:
    request_id: str
    data: str | Image
