from io import BytesIO
from typing import Tuple
from rembg import remove
from utils import Request, Response, load_model
import base64
from fastapi.concurrency import run_in_threadpool

SESSION = load_model("u2net")

from PIL import Image


class BackgroundRemove:
    @staticmethod
    def process_image(image: Image.Image) -> Tuple[Image.Image | None, str]:
        try:
            input: Image.Image = image.convert("RGBA")
        except Exception:
            error_data = "error opening data"
            return None, error_data
        try:
            output = remove(input, session=SESSION)
            match output:
                case Image.Image():
                    final_out = output.convert("RGBA")
                    error_data = ""
                case _:
                    final_out = None
                    error_data = "error converting output image"

            return final_out, error_data

        except Exception:
            error_data = "error process the image"
            return None, error_data

    @staticmethod
    async def run(request: Request):
        response = Response(
            request_id="",
            success=True,
            data="",
            error_message="",
        )
        try:
            decode_base64 = BytesIO(base64.b64decode(request.data))
            image = Image.open(decode_base64)
            if image.format not in ["JPEG", "JPG", "PNG", "TIFF", "BMP"]:
                response.success = False
                response.error_message = "Invalid Request image not in correct format"
        except Exception:
            response.success = False
            response.error_message = "Invalid Request can not decode the input data"
            return response
        if response.success:
            try:
                output, error = await run_in_threadpool(
                    BackgroundRemove.process_image, image
                )
                if output:
                    buffer = BytesIO()
                    output.save(buffer, format="png")
                    response.data = base64.b64encode(buffer.getvalue()).decode()
                else:
                    response.success = False
                    response.error_message = error
                return response
            except Exception as e:
                response.success = False
                response.error_message = f"Error processing data {e}"
                return response
        else:
            response.error_message = "Invalid Request error with file format"
            return response
