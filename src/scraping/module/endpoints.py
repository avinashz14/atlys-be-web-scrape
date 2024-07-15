from fastapi import APIRouter

router = APIRouter()


@router.get("/healthcheck")
async def healthcheck(user_id: int):
    print(user_id)
    return {
        "status": 0,
        "message": "SUCCESS",
        "data": {
            "user_id": user_id
        }
    }
