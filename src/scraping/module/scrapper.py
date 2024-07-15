from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter, Body, Request

from src.libs.auth_package import auth_required
from src.scraping.controllers.director_scrapper_controller import ScrapperDirectorController
import uuid

router = APIRouter()


class ScrapeRequest(BaseModel):
    url: str
    proxy: str = ""
    page: int = 1
    limit: int = 1


@router.post("/api/v1/scrape/")
@auth_required
async def create_scrapping_request(request: Request, request_data: ScrapeRequest = Body(...)):
    # collect request and process in bg process.
    task_id = str(uuid.uuid4())
    # make single instance for unique request and duplicate site request refuse as already in queue for process.
    ctl = ScrapperDirectorController(url=request_data.url, proxy=request_data.proxy, page=request_data.page, limit=request_data.limit,
                                     task_id=task_id)
    data, err = ctl.do()
    if err:
        return {
            "status": 0,
            "message": "FAILED",
            "data": data,
            "err": str(err)
        }
    return {
        "status": 0,
        "message": "SUCCESS",
        "data": {
            **data,
            "task_id": task_id
        }
    }
