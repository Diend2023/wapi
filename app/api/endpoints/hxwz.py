"""
HXWZ 口令验证接口
目录：/hxwz/
"""
from fastapi import APIRouter, HTTPException
from app.services.hxwz_service import (
    get_current_token, encrypt_token, verify_token
)
from app.schemas.hxwz import (
    HxwzGetTokenResponse, HxwzCheckTokenRequest, HxwzCheckTokenResponse
)

router = APIRouter()


@router.get(
    "/hxwz/get_token",
    response_model=HxwzGetTokenResponse,
    status_code=200,
    tags=["HXWZ"],
)
async def get_token():
    """
    获取加密口令。
    服务端返回当前存储的口令经 XOR 加密后的 base64 字符串。
    若未配置口令，返回 404。
    """
    token = get_current_token()
    if token is None:
        raise HTTPException(status_code=404, detail="口令未配置")

    encrypted = encrypt_token(token)
    return {
        "code": 200,
        "msg": "获取成功",
        "data": {"encrypted_token": encrypted},
    }


@router.post(
    "/hxwz/check_token",
    response_model=HxwzCheckTokenResponse,
    status_code=200,
    tags=["HXWZ"],
)
async def check_token(req: HxwzCheckTokenRequest):
    """
    验证口令。
    用户提交明文口令，服务端验证是否正确。
    验证成功返回明文和加密口令，供客户端对比校验。
    """
    # 验证用户输入的明文
    verify_result = verify_token(req.plaintext)
    if not verify_result.get("success", False):
        raise HTTPException(status_code=401, detail=verify_result.get("error", "口令验证失败"))

    # 验证通过：返回明文 + 加密口令（供客户端二次校验）
    token = verify_result["plaintext"]
    encrypted = verify_result["encrypted"]
    return {
        "code": 200,
        "msg": "验证成功",
        "data": {
            "plaintext": token,
            # "encrypted_token": encrypted,
        },
    }
