from PIL import Image
from rembg import new_session, remove
from fastapi import FastAPI, File, Response, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from io import BytesIO
import base64

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

@app.post("/uploadFile/")
async def upload_file(file: UploadFile):
    if "image" in str(file.content_type):
        SESSION =await load_model('u2net')
        data = BytesIO(file.file.read())
        image = Image.open(data).convert("RGBA")

        output_image: Image.Image = remove(image, session=SESSION).convert("RGBA")
        buffer = BytesIO()
        # output_image.save('./result.png', format='PNG')
        output_image.save(buffer, format='png')
        buffer.seek(0)

        # return FileResponse(path="./result.png")
        # return Response(content= output_image, media_type='image/png')
        # return Response(
        #     content= buffer.getvalue(),
        #     media_type= 'image/png'
        # )
        return StreamingResponse(buffer, media_type='image/png')
    else:
        return {
            "error": "file is not a image"
        }

@app.post("/encode_file/")
async def encode_file(payload: bytes):
    SESSION = await load_model('u2net')
    image = Image.open(payload).convert("RGBA")

    output_image: Image.Image = remove(image, session=SESSION).convert("RGBA")
    buffer = BytesIO()
    output_image.save(buffer, format='png')
    base64_output = base64.b64encode(buffer.getvalue()).decode()
    return {
        "result": base64_output,
    }
