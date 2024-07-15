from fastapi import FastAPI
from src.scraping.module import endpoints, scrapper, task


app = FastAPI()

origin = [
    "*"
]

# include middlewares

# include routers
app.include_router(endpoints.router)
app.include_router(scrapper.router)
app.include_router(task.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
