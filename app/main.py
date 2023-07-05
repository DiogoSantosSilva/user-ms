from fastapi import FastAPI
from app.controllers import user_controller

app = FastAPI()

app.include_router(user_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)