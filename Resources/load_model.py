from rembg import new_session

def load_model(name:str):
    _Model_PATH = 'model/u2net.onnx'
    _Model_PATH = _Model_PATH.split("/")[-1]
    print(_Model_PATH)
    if name == _Model_PATH:
        session = new_session(model_name=_Model_PATH)
    else:
        raise RuntimeError(
            f"Model {name} not found"
        )
        
    return session