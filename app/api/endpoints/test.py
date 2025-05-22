from fastapi import APIRouter

router = APIRouter()

@router.get("/test", tags=["Test"])
async def read_sample():
    return {"message": "This is a test endpoint."}