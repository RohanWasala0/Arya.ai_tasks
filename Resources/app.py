from resources.bgremove_process import BackgroundRemover
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class PayloadRequest(BaseModel):
    req_id: str
    doc_base64: str
    bg_color: list

@app.post("/bg_remove")
async def remove_background(request:PayloadRequest):
    try:
        # img = base64.b64decode(request.img_b64).decode('utf-8')
        # print(img)
        req_id =  request.req_id
        doc_base64 = request.doc_base64
        bg_color = request.bg_color
        request_dict = {"req_id": req_id, "doc_base64": doc_base64, "bg_color": bg_color}
        # Process the request
        # print(request_dict)
        response = await BackgroundRemover.run(request_dict)
        if response["error_message"] is None:
            return JSONResponse(content=response, status_code=200)
        else:
            return JSONResponse(content=response, status_code=400)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Bad Request!")