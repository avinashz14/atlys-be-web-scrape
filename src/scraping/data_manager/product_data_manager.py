from src.scraping.models import Product
# from fastapi import FastAPI, HTTPException
import json
from pathlib import Path


class ProductDataManager:
    Path("data").mkdir(parents=True, exist_ok=True)
    file_path = "data/product_data.json"
    products = []

    def load_product(self):
        '''

        :return:
        :rtype:
        '''
        # Load existing product from the JSON file if it exists
        if Path(self.file_path).exists():
            with open(self.file_path, "r") as file:
                try:
                    self.products = json.load(file)
                except json.JSONDecodeError:
                    self.products = []
        else:
            self.products = []

    def save_product(self, product: Product):
        '''
        0 --> Duplicate or failed to update.
        1 --> New product added.
        2 --> Product updated added.
        :param product:
        :type product:
        :return:
        :rtype:
        '''
        # Check for duplicate product by ID
        is_updated = 0
        for existing_product in self.products:
            if existing_product["id"] == product.id:
                if product.price == existing_product["price"]:
                    print(f"Duplication data found")
                    return 0
                else:
                    existing_product["price"] = product.price
                    # self.update_product(product)
                    is_updated = 1
                    break

        # Add the new product to the list
        if not is_updated:
            self.products.append(product.dict())

        # Save the updated list back to the JSON file
        try:
            with open(self.file_path, "w") as file:
                json.dump(self.products, file, indent=4)
            return 2 if is_updated else 1
        except Exception as e:
            print(f"Err: while storing data in product json file, {e}")
            return 0

    def update_product(self, product: Product):
        pass
