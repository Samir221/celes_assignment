from fastapi.responses import JSONResponse
from fastapi.requests import Request
import uvicorn
import firebase_admin
from firebase_admin import credentials, auth
import pyrebase
from fastapi import FastAPI
import firebase_admin.auth
from fastapi import HTTPException
import json
# from .firebase_config import firebaseConfig  - imported as secrets in github
from dotenv import load_dotenv
import os


firebaseConfig = {
  "apiKey": os.getenv("FIREBASE_API_KEY"),
  "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
  "projectId": os.getenv("FIREBASE_PROJECT_ID"),
  "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
  "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
  "appId": os.getenv("FIREBASE_APP_ID"),
  # "databaseURL": os.getenv("FIREBASE_DATABASE_URL") # Uncomment if you have this
}


load_dotenv()


if not firebase_admin._apps:
    cred = credentials.Certificate("celes_microservice/credentials.json")
    firebase_admin.initialize_app(cred) 


firebase = pyrebase.initialize_app(firebaseConfig)


app = FastAPI(
    description="Login endpoint for celes assignment.",
    title="Firebase_Auth",
    docs_url="/"
)


async def validate_token(request: Request):
    headers = request.headers
    auth_header = headers.get('authorization')
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")

    jwt_token = auth_header.split(" ")[1]

    try:
        user = auth.verify_id_token(jwt_token)
        return user
    except firebase_admin.auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid ID token")
    except firebase_admin.auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Expired ID token")
    except Exception as e:  # Catch other potential exceptions
        raise HTTPException(status_code=401, detail=str(e))


@app.post('/login')
async def create_access_token():
    username = os.environ.get("FIREBASE_USERNAME")
    password = os.environ.get("FIREBASE_PASSWORD")

    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email=username,
            password=password
        )
        token = user.get('idToken')
        return JSONResponse(content={"token": token}, status_code=200)
    
    except:
        raise HTTPException(status_code=400, details="Invalid Credentials.")

 
async def get_valid_token():
    token_response = await create_access_token()
    content_bytes = token_response.body 
    content_str = content_bytes.decode('utf-8')
    json_content = json.loads(content_str) 
    return json_content


if __name__ == "__main__":
    uvicorn.run("firebase_auth:app",reload=True)
