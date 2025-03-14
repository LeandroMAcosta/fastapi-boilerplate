from fastapi import APIRouter, Depends

from modules.user.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
async def get_user(user_id: int, service: UserService = Depends()):
    return await service.get_by_id(user_id)
