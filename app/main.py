from dataclasses import asdict
from PIL import Image
from pydantic import BaseModel
from rembg import new_session, remove
from fastapi import FastAPI, File, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from io import BytesIO
import base64

from utils import Request
from BackgroundRemove import BackgroundRemove

async def load_model(name:str):
    _Model_PATH = 'model/u2net.onnx'
    _Model_PATH = _Model_PATH.split("/")[-1]
    _Model_PATH = _Model_PATH.split(".")[0]
    print(_Model_PATH)
    if name == _Model_PATH:
        session = new_session(model_name=_Model_PATH)
    else:
        raise RuntimeError(
            f"Model {name} not found"
        )

    return session

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "something something temp"}

# @app.post("/uploadFile/")
# async def upload_file(file: UploadFile):
#     if "image" in str(file.content_type):
#         data = BytesIO(file.file.read())
#         image = Image.open(data).convert("RGBA")
#
#         output_image: Image.Image = remove(image, session=SESSION).convert("RGBA")
#         buffer = BytesIO()
#         # output_image.save('./result.png', format='PNG')
#         output_image.save(buffer, format='png')
#         buffer.seek(0)
#
#         # return FileResponse(path="./result.png")
#         # return Response(content= output_image, media_type='image/png')
#         # return Response(
#         #     content= buffer.getvalue(),
#         #     media_type= 'image/png'
#         # )
#         return StreamingResponse(buffer, media_type='image/png')
#     else:
#         return {
#             "error": "file is not a image"
#         }

class PayloadRequest(BaseModel):
    request_id: str
    data: str

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
