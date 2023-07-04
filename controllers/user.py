from services.user import create_user
from main import app


@app.post("/users")
def create_user(data):
    return create_user
