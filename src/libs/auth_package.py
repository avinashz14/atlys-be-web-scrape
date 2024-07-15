from fastapi import FastAPI, Request, HTTPException
from functools import wraps

app = FastAPI()

# Static authentication key
STATIC_AUTH_KEY = "0964-4204-atlys-be-4bf8b973-8b91-05d47ae57f8e"


# Generalized decorator for API authentication
def auth_required(f: object) -> object:
    @wraps(f)
    async def decorated_function(request: Request, *args, **kwargs):
        auth_key = request.headers.get('Authorization')
        if auth_key != STATIC_AUTH_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")
        data = await f(request, *args, **kwargs)
        return data

    return decorated_function
