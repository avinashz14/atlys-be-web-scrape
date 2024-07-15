from src.scraping.models import Product, Task
import json
from pathlib import Path


class TaskDataManager:
    Path("data").mkdir(parents=True, exist_ok=True)
    file_path = "data/task_data.json"
    tasks = []

    def load_task(self):
        '''

        :return:
        :rtype:
        '''
        # Load existing tasks from the JSON file if it exists

        if Path(self.file_path).exists():
            with open(self.file_path, "r") as file:
                try:
                    self.tasks = json.load(file)
                except json.JSONDecodeError:
                    self.tasks = []
        else:
            self.tasks = []

    def get_task_by_id(self, task_id: str):
        self.load_task()
        for existing_task in self.tasks:
            if existing_task["id"] == task_id:
                return existing_task
        return {}

    def update_task_by_id(self, task_id: str, task_data: dict):
        self.load_task()
        updated_data = None
        for existing_task in self.tasks:
            if existing_task["id"] == task_id:
                existing_task.update(**task_data)
                updated_data = existing_task
                break
        print(task_data, updated_data)
        self.store_data_json_file()
        return updated_data

    def create_task(self, unique_id: str, task_data: dict = {}):
        err = None
        self.load_task()
        task = Task(id=unique_id, **task_data)
        self.save_task(task)
        return task, err

    def save_task(self, task: Task):
        '''
        :param task:
        :type task:
        :return:
        :rtype:
        '''
        # Check for duplicate task by ID
        is_updated = 0
        for existing_task in self.tasks:
            if existing_task["id"] == task.id:
                existing_task.update(task.dict())
                # self.update_product(task)
                is_updated = 1
                break

        # Add the new task to the list
        if not is_updated:
            self.tasks.append(task.dict())

        self.store_data_json_file()

    # Save the updated list back to the JSON file
    def store_data_json_file(self):
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.tasks, file, indent=4)
            return 1
        except Exception as e:
            print(f"Err: while storing data in task json file, {e}")
            return 0

    def update_product(self, product: Product):
        pass
