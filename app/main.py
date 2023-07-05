from fastapi import FastAPI
from app.controllers import user_controller, authentication_controller
from app.config import settings

app = FastAPI()

app.include_router(user_controller.router)
app.include_router(authentication_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)