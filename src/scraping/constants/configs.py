from dataclasses import dataclass


@dataclass
class Response:
    status: int
    message: str


class Config:
    class Missing:
        pass

    class Invalid:
        INVALID_OPERATION = Response(1, "Invalid operation, make sure operation valid")
