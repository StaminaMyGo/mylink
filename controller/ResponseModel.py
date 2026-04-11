from pydantic import BaseModel
class ResponseModel:

    def __init__(self, code: int = 2000, msg: str = "success", data = None):
        self.code=code
        self.msg=msg
        self.data=data
