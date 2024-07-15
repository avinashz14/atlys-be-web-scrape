from fastapi import APIRouter, Request

from src.libs.auth_package import auth_required
from src.scraping.controllers.task_controller import TaskController

router = APIRouter()


@router.get("/api/v1/result/{task_id}")
@auth_required
async def get_result(request: Request, task_id: str):
    ctl = TaskController()
    task_result = ctl.get_task(task_id)
    # if task_result.status == 'PENDING':
    #     return {"status": "Pending"}
    # elif task_result.state != 'FAILURE':
    #     return {"status": task_result.state, "result": task_result.result}
    # else:
    #     return {"status": "Failure", "error": str(task_result.info)}
    return {
        "status": 0,
        "message": "SUCCESS",
        "data": {
            **task_result
        }
    }
