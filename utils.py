from dataclasses import dataclass
from rembg import new_session
import os
import psutil

SESSION_LOG = "/temp/session_creation.txt"

def load_model(name:str):
    _Model_PATH = 'model/u2net.onnx'
    _Model_PATH = _Model_PATH.split("/")[-1]
    _Model_PATH = _Model_PATH.split(".")[0]
    print(_Model_PATH)
    if name == _Model_PATH:
        session = new_session(model_name=_Model_PATH)

        #for testing sessions Logs session creation 
        pid = os.getpid()
        mem = psutil.Process(pid).memory_info().rss
        with open(SESSION_LOG, "a") as log:
            log.write(f"Process ID:{pid}, Memory:{mem} SESSION LOADED\n")
    else:
        raise RuntimeError(
            f"Model {name} not found"
        )

    return session

@dataclass
class Response:
    request_id: str
    success: bool
    data: str
    error_message: str

@dataclass
class Request:
    request_id: str
    data: str
