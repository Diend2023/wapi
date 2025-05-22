from typing import Optional
from pydantic import BaseModel

class MinecraftResponse(BaseModel):
    code: int
    msg: str
    data: Optional[dict] = None