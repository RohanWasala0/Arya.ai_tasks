from requests import request
from utils import Request, Response, make_base64
import uuid
import httpx
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
ImageQualityToken = os.environ.get('ImageQualityToken')
HologramToken = os.environ.get('HologramToken')
SignToken = os.environ.get('SignToken')

TASK2_LOG = './temp/API_LOG.log'

class ImageHologramSign:
    client = httpx.AsyncClient(timeout= 10)
    request_id = ''
    data = {}

    @classmethod
    async def image_quality(cls, doc_base64) -> bool:
        url = "https://ping.arya.ai/api/v1/image-quality"
        payload = {
            'doc_base64': doc_base64,
            'req_id': cls.request_id
        }
        header = {
            'token': ImageQualityToken,
            'content-type': 'application/json'
        }

        try:
            response = await cls.client.post(url= url, json= payload, headers= header)
            response.raise_for_status()
        except httpx.HTTPError as e:
            print("Request failed:", e)
            return False

        if data := response.json().get('data'):
            cls.data['image quality data'] = response.json()
            return int(data.get('background_uniformity_score')) > 50
        else:
            print('something is wrong')
            return False

    @classmethod
    async def check_hologram(cls, doc_base64, crop: bool):
        url = "https://ping.arya.ai/api/v1/hologram-detection"
        payload = {
            'doc_base64': doc_base64,
            'crop': crop,
            'req_id': cls.request_id
        }
        header = {
            'token': HologramToken,
            'content-type': 'application/json'
        }
        try:
            response = await cls.client.post(url= url, json= payload, headers= header)
            response.raise_for_status()
        except httpx.HTTPError as e:
            print("Request failed:", e)
            return
        cls.data['hologram data'] = response.json()

    @classmethod
    async def check_signature(cls, doc_base64):
        url = "https://ping.arya.ai/api/v2/signature-detection"
        payload = {
            'output_format': 'snippets',
            'doc_base64': doc_base64,
            'req_id': cls.request_id
        }
        header = {
            'token': SignToken,
            'content-type': 'application/json'
        }

        try:
            response = await cls.client.post(url= url, json= payload, headers= header)
            response.raise_for_status()
        except httpx.HTTPError as e:
            print("Request failed:", e)
            return
        cls.data['signature data'] = response.json()

    @classmethod
    async def close(cls):
        await cls.client.aclose()

    @staticmethod
    async def run(request: Request) -> Response:
        response: Response = Response(
            request_id= request.request_id,
            success= True,
            data= '',
            error_message= ''
        )
        ImageHologramSign.request_id = request.request_id
        if response.success:
            try: 
                quality_good = await ImageHologramSign.image_quality(doc_base64= request.data)
            except Exception as e:
                response.success = False
                response.data = str(ImageHologramSign.data)
                response.error_message = f'Invalid Request Body with {e}'
                await ImageHologramSign.close()
                return response
            if quality_good:
                asyncio.gather(
                    ImageHologramSign.check_hologram(doc_base64= response.data, crop= True),
                    ImageHologramSign.check_signature(doc_base64= response.data)
                )
                response.success = True
                response.data = str(ImageHologramSign.data)
                await ImageHologramSign.close()
                return response
            else:
                response.success = False
                response.data = str(ImageHologramSign.data)
                response.error_message = 'Document quality bad'
                await ImageHologramSign.close()
                return response
        await ImageHologramSign.close()
        return response

