from fastapi import APIRouter, HTTPException
from app.services.delta_force.get_ovd_data import get_ovd_data
from app.schemas.delta_force import DeltaForceResponse

router = APIRouter()


@router.get(
    "/delta_force/ovd_data",
    response_model=DeltaForceResponse,
    status_code=200,
    tags=["DeltaForce"]
)
async def ovd_data():
    result = await get_ovd_data()
    if not result:
        raise HTTPException(status_code=400, detail="get failed")
    return {
        "code": 200,
        "msg": "获取成功",
        "data": result.get("data", [])
    }
