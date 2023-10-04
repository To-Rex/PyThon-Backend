from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
import bcrypt

# Create a FastAPI app
app = FastAPI()


# Define a Pydantic model for user input
class UserLogin(BaseModel):
    email: str
    password: str


# Define a Pydantic model for user response
class UserResponse(BaseModel):
    token: str


# Dummy database representing user records
users_db = [
    {
        "id": 1,
        "email": "user@example.com",
        "password_hash": b'$2b$12$Zs6IlMWkm61so9/sOWZJ6.b4BHDg9T1C6pho1jNxyClhCfysjho2.',
    },
    # Add more user records as needed
]

# Secret key for JWT token generation (replace with your own secret key)
SECRET_KEY = "your-secret-key"

# Token expiration time (e.g., 1 hour)
TOKEN_EXPIRATION = timedelta(hours=1)


# Function to generate a JWT token
def generate_token(user_id: int) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + TOKEN_EXPIRATION,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


# Route for user login
@app.post("/login", response_model=UserResponse)
async def login(user_data: UserLogin):
    # Check if user exists in the database
    user = next((u for u in users_db if u["email"] == user_data.email), None)
    if not user or not bcrypt.checkpw(user_data.password.encode(), user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate a JWT token
    token = generate_token(user["id"])

    return {"token": token}
