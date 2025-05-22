from typing import Optional
from pydantic import BaseModel

class DeltaForceResponse(BaseModel):
    code: int
    msg: str
    data: Optional[dict] = None