from src.scraping.controllers.base_scrapper import BaseScrapperController
from src.scraping.data_manager.tasks_data_manager import TaskDataManager


class TaskController:

    def get_task(self, task_id: str):
        task_data_ctl = TaskDataManager()
        task = task_data_ctl.get_task_by_id(task_id)
        return task
