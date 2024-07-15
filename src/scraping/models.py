from pydantic import BaseModel


# Define the data model
class Product(BaseModel):
    id: str
    title: str = None
    image_url: str = None
    # rating: int
    price: float
    original_price: float = None
    # description: str


class Task(BaseModel):
    id: str
    requester_id: int = None
    title: str = None
    url: str = None
    proxy: str = None
    page: int = 1
    limit: int = 1
    meta_data: dict = {}
    status: str = "INITIATED"
