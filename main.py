from dataclasses import asdict
from httpx import request
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from ImageHologramSign import ImageHologramSign
from utils import Request
from BackgroundRemove import BackgroundRemove

class PayloadRequest(BaseModel):
    request_id: str
    data: str

app = FastAPI()

import time
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    print(response.headers)
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response

@app.post("/background_remove/")
async def encode_file(payload: PayloadRequest):
    try:
        request = Request(
            request_id= payload.request_id,
            data= payload.data
        )

        response = await BackgroundRemove.run(request)
        if response.error_message == "":
            return JSONResponse(content= asdict(response))
        else:
            return JSONResponse(content= asdict(response), status_code= 400)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Bad Request!!!!!!")

@app.post('/image_hologram_sign/')
async def gather(payload: PayloadRequest):
    try:
        request = Request(
            request_id= payload.request_id,
            data= payload.data
        )

        response = await ImageHologramSign.run(request)
        if response.error_message == "":
            return JSONResponse(content= asdict(response))
        else:
            return JSONResponse(content= asdict(response), status_code= 400)
    except Exception as e:
        print(e)
        raise HTTPException(status_code= 500, detail="Bad Request!!!!")
