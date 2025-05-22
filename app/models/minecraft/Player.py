import base64
import json
from pydantic import BaseModel


class Player(BaseModel):
    name: str
    uuid: str
    value: str
    legacy: bool = False
    demo: bool = False

    def decode_value(self):
        """
        Decode the value attribute from base64 to json.
        """
        decoded_bytes = base64.b64decode(self.value)
        decoded_str = decoded_bytes.decode('utf-8')
        decoded_json = json.loads(decoded_str)
        return decoded_json