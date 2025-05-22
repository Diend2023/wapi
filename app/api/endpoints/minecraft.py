from fastapi import APIRouter, HTTPException
from app.services.minecraft.mojang import get_uuid, get_profile
from app.schemas.minecraft import MinecraftResponse

router = APIRouter()

@router.get(
    "/minecraft/uuid/{name}",
    response_model=MinecraftResponse,
    status_code=200,
    tags=["Minecraft"]
)
async def uuid(name: str):
    """
    获取玩家的UUID
    \nparam name: 玩家名称
    \nreturn: UUID
    """
    result = get_uuid(name)
    if not result:
        raise HTTPException(status_code=400, detail="名称不存在")
    return {
        "code": 200,
        "msg": "获取成功",
        "data": result
    }


@router.get(
    "/minecraft/profile/{name}",
    response_model=MinecraftResponse,
    status_code=200,
    tags=["Minecraft"]
)
async def profile(name: str):
    """
    获取玩家的皮肤和头像
    \nparam name: 玩家名称
    \nreturn: 皮肤和头像的URL
    """
    Player = get_profile(name)
    if not Player:
        raise HTTPException(status_code=400, detail="名称不存在")
    result = {
        "name": Player.name,
        "uuid": Player.uuid,
        "legacy": Player.legacy,
        "demo": Player.demo,
        "value": Player.decode_value(),
    }
    return {
        "code": 200,
        "msg": "获取成功",
        "data": result
    }