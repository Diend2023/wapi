from typing import Optional
from pydantic import BaseModel


class HxwzGetTokenResponse(BaseModel):
    code: int
    msg: str
    data: Optional[dict] = None


class HxwzCheckTokenRequest(BaseModel):
    plaintext: str


class HxwzCheckTokenResponse(BaseModel):
    code: int
    msg: str
    data: Optional[dict] = None
