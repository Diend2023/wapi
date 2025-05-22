from fastapi import Depends, HTTPException
# from sqlalchemy.orm import Session
# from app.core.config import get_db

# def get_current_user(db: Session = Depends(get_db)):
#     # 这里可以添加获取当前用户的逻辑
#     pass

def get_query_param(param: str):
    if not param:
        raise HTTPException(status_code=400, detail="Query parameter is required")
    return param