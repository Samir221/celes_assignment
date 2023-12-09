import firebase_admin
from firebase_admin import credentials, auth
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
import secrets


app = FastAPI()
SECRET_KEY = secrets.token_urlsafe(32) 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Initialize Firebase Admin SDK
cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred) 


# Pydantic model for request body
class UserLogin(BaseModel):
    username: str
    password: str


# Function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Endpoint to verify username and password and generate JWT token
@app.post('/login')
async def login(user_data: UserLogin):
    try:

        user = auth.get_user_by_email(user_data.username)
        # Use Firebase's built-in password verification
        #firebase_admin.auth.verify_password(user.uid, user_data.password)
        auth.verify_password(user.uid, user_data.password)
        expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.uid}, expires_delta=expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=401, detail='Invalid username or password')


def main():
    # Create a test client for the FastAPI app
    client = TestClient(app)

    # Dummy user data
    dummy_data = {
        "username": "sammy@test.com",
        "password": "123456"
    }

    # Call the login endpoint using the test client
    response = client.post("/login", json=dummy_data)

    # Print the response from the login endpoint
    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    from fastapi.testclient import TestClient
    main()