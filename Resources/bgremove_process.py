from rembg import remove
from PIL import Image
import base64
from io import BytesIO
from utils.load_model import load_model

SESSION = load_model('u2net.onnx')

class BackgroundRemover:
    
    @staticmethod
    def remove_background(image, bg_color):
        error_data = ""
        try:
            # print("2")
            input_image = image.convert("RGBA")  
        except Exception as e:
            error_data = "Data cannot be opened."
            return None, error_data
        try:
            # print(bg_color)
            if bg_color:
                if len(bg_color) < 3:
                    error_data = "Invalid format."
                    return None, error_data
                if any(n < 0 for n in bg_color):
                    error_data = "Invalid format."
                    return None, error_data
                bg_color.append(255)
                output_image = remove(input_image, session=SESSION, bgcolor=bg_color)
                # end = time.time()
                # print("Time Taken for Processing: ", end-start)
                output_image = output_image.convert("RGBA")
                buffered = BytesIO()
                output_image.save(buffered, format="PNG")
                base64_output = base64.b64encode(buffered.getvalue()).decode()
                return base64_output, error_data
            else:
                output_image = remove(input_image, session=SESSION)
                # end = time.time()
                # print("Time Taken for Processing: ", end-start)
                output_image = output_image.convert("RGBA")
                buffered = BytesIO()
                output_image.save(buffered, format="PNG")
                base64_output = base64.b64encode(buffered.getvalue()).decode()
                return base64_output, error_data
        except Exception as e:
            error_data = "Error processing data."
            return None, error_data
        
    @staticmethod
    async def run(request_dict):
        error_message = "Invalid Request"
        FLAG = True
        error_message = ''
        response = {'req_id': '', "success": FLAG, "data":{}, "error_message": error_message}
        try:
            req_id = request_dict.get('req_id')
            doc_base64 = request_dict.get('doc_base64')
            bg_color = request_dict.get('bg_color')
            response["req_id"] = req_id
            decoded_data = BytesIO(base64.b64decode(doc_base64))
            image = Image.open(decoded_data)
            
            if image.format not in ["JPEG", "JPG", "PNG", "TIFF", "BMP"]:
                FLAG = False
                error_message = "Invalid input provided."
                response["success"] = FLAG
                response["error_message"] = error_message
                return response
        except Exception as e:
            FLAG = False
            error_message = "Invalid input."
            response["success"] = FLAG
            response["error_message"] = error_message
            return response
        if FLAG:
            try:
                base64_output, error_data = BackgroundRemover.remove_background(image, bg_color)
                if base64_output:
                    FLAG = True
                    response["success"] = FLAG
                    response["data"]["doc_base64"] = base64_output
                    response["error_message"] = None
                    return response
                else:
                    FLAG = True
                    error_message = error_data
                    response["success"] = FLAG
                    response["error_message"] = error_data
                    return response
            except Exception as e:
                error_message = "Error occured while execution."
                FLAG = True
                response["error_message"] = error_message
                response["success"] = FLAG
                return response
        else:
            error_message = "Invalid input format"
            response["error_message"] = error_message
            response["success"] = FLAG
            return response
        
            
            
            

    

