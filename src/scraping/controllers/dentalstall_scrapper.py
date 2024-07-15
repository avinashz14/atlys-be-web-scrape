from src.scraping.controllers.base_scrapper import BaseScrapperController
from src.scraping.constants.constants import Constant
from src.scraping.controllers.scrapper import ProductSpider
import subprocess

from src.scraping.data_manager.tasks_data_manager import TaskDataManager


class DentalstallScrapperController(BaseScrapperController):

    def __init__(self, *args, **kwargs):
        super(DentalstallScrapperController, self).__init__(*args, **kwargs)
        self.scrapping_site = Constant.ScrappingSite.Dentalstall.value
        self.result = None
        self.error = None  # TODO: can define error map for this.

    def scrape(self):
        try:
            command = ["scrapy", "runspider", "src/scraping/controllers/scrapper.py", "-a",
                       f"url={self.url}", "-a", f"task_id={self.task_id}", "-a", f"limit={self.limit}"]
            if self.proxy:
                command.append(f"-a proxy={self.proxy}")
            a = subprocess.run(command, check=True)
            print(a)
            return {"status": "success", "message": "Scraping completed", "task": self.task.dict()}, None
        except subprocess.CalledProcessError as e:
            # raise HTTPException(status_code=500, detail=str(e))
            return None, e

    def get_next_page(self, page: int):
        pass

    def get_proxy(self):
        pass

    def validate_site_specific_data(self):
        self.validate_product_data()

    def validate_product_data(self):
        pass
