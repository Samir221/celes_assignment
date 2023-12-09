from fastapi.responses import JSONResponse
from fastapi.requests import Request
import jwt
from jwt import PyJWTError
import uvicorn
from fastapi import FastAPI
import firebase_admin
from firebase_admin import credentials, auth
import pyrebase
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
import firebase_admin.auth
from fastapi import HTTPException


if not firebase_admin._apps:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred) 


firebaseConfig = {
  "apiKey": "AIzaSyDYPmn0gy6IlxkH3Wd5tVvcBs2CnLbt83Y",
  "authDomain": "celes-queries.firebaseapp.com",
  "projectId": "celes-queries",
  "storageBucket": "celes-queries.appspot.com",
  "messagingSenderId": "191358285229",
  "appId": "1:191358285229:web:69d4e2792e49e285935d24",
  "databaseURL": ""
}


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
        #user = firebase_admin.auth.verify_id_token(jwt_token)
        user = auth.verify_id_token(jwt_token)
        #return user.uid
        return user
    except firebase_admin.auth.InvalidIdTokenError:
        raise HTTPException(status_code=401, detail="Invalid ID token")
    except firebase_admin.auth.ExpiredIdTokenError:
        raise HTTPException(status_code=401, detail="Expired ID token")
    except Exception as e:  # Catch other potential exceptions
        raise HTTPException(status_code=401, detail=str(e))


@app.post('/login')
async def create_access_token():
    USERNAME = "sammy@test.com"
    PASSWORD = "123456"
    try:
        user = firebase.auth().sign_in_with_email_and_password(
            email = USERNAME,
            password = PASSWORD
        )
        token = user.get('idToken')
        return JSONResponse(content={"token": token}, status_code=200)
    
    except:
        raise HTTPException(status_code=400, details="Invalid Credentials.")



if __name__ == "__main__":
    uvicorn.run("firebase_auth:app",reload=True)
