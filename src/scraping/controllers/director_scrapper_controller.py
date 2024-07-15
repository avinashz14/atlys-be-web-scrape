from src.libs.api_exception import BadRequest
from src.scraping.constants.configs import Config
from src.scraping.constants.constants import Constant
from src.scraping.controllers.dentalstall_scrapper import DentalstallScrapperController


class ScrapperDirectorController:

    def __init__(self, *args, **kwargs):
        self.task_id = kwargs.get("task_id")
        self.requester_id = kwargs.get("requester_id")

    def __new__(cls, url: str, proxy: str = None, *args, **kwargs):
        appropriate_controller = None

        if Constant.ScrappingSite.Dentalstall.value in url.lower():
            appropriate_controller = DentalstallScrapperController(url=url, proxy=proxy, *args, **kwargs)

        if not appropriate_controller:
            error = Config.Invalid.INVALID_OPERATION
            response = {"status": error.status, "message": error.message}
            raise BadRequest(response)

        return appropriate_controller
