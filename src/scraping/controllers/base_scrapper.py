from abc import ABC, abstractmethod

from src.scraping.data_manager.tasks_data_manager import TaskDataManager
from src.scraping.models import Task


class BaseScrapperController(ABC):

    def __init__(self, *args, **kwargs):
        self.task_id = kwargs.get("task_id")
        self.url = kwargs.get("url")
        self.proxy = kwargs.get("proxy")
        self.limit = kwargs.get("limit")
        self.scrapping_site = None
        self.task = None
        self.result = None
        self.error = None

    def do(self):
        task, err = self.create_new_task()
        if err:
            return task, err
        data, err = self.scrape()
        return data, err

    def create_new_task(self):
        task_data_ctl = TaskDataManager()
        task_data = {
            "url": self.url,
            "limit": self.limit,
            "proxy": self.proxy
        }
        self.task, err = task_data_ctl.create_task(self.task_id, task_data=task_data)
        return self.task, err

    @abstractmethod
    def scrape(self):
        pass

    def validate_scrapped_data(self):
        pass

    @abstractmethod
    def validate_site_specific_data(self):
        pass

    def track_session_stats(self):
        pass
