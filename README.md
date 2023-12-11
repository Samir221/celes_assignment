**
# Celes Assignment

## Overview

Celes Assignment is a Python-based project developed to create authenticated endpoints that perform queries on a dataset of parquet files. The project leverages FastAPI for building APIs and Firebase for authentication, ensuring secure and efficient data handling.

## Prerequisites

-   Python (preferably the latest version)
-   Firebase Account
-   FastAPI
-   Uvicorn
-   Pytest for running unit tests

## Setting Up Firebase Authentication

1.  **Create a Firebase Project**: Go to the [Firebase Console](https://console.firebase.google.com/) and create a new project.
    
2.  **Download Credentials**:
    
    -   Navigate to the Project settings > Service accounts.
    -   Click on "Generate new private key" and download the `credentials.json` file.
    -   Place this file in the root directory of the project.
3.  **Create Verified User**:
    
    -   In Firebase, set up authentication (Email/Password) and create a user.
    -   Store the user's email and password in a `.env` file in the root directory of the project with the keys `FIREBASE_USERNAME` and `FIREBASE_PASSWORD`.


## Setting Up Firebase Configuration

1.  **Retrieve Firebase Configuration Data**:
    
    -   Go to the [Firebase Console](https://console.firebase.google.com/).
    -   Select your project.
    -   Click on the gear icon next to "Project Overview" and choose "Project settings".
    -   Under "Your apps", select the app for which you want the configuration.
    -   Here, you'll find your Firebase configuration object (`firebaseConfig`).
2.  **Create Firebase Configuration File**:
    
    -   Create a file named `firebase_config.py` in the `celes_microservice` folder of your project.
        
    -   Copy your Firebase configuration data into this file in the following format:
        
        pythonCopy code
        
        `# celes_microservice/firebase_config.py
        firebaseConfig = {
          "apiKey": "your-api-key",
          "authDomain": "your-project-id.firebaseapp.com",
          "projectId": "your-project-id",
          "storageBucket": "your-project-id.appspot.com",
          "messagingSenderId": "your-messaging-sender-id",
          "appId": "your-app-id",
          "databaseURL": "your-database-url"
        }` 
        
    -   Replace the placeholder values with your actual Firebase project settings.
        
3.  **Using Firebase Configuration in Your Application**:
    
    -   Import this configuration into your application wherever you need to initialize Firebase:
        
        pythonCopy code
        
        `from .firebase_config import firebaseConfig
        
4.  **Securing Configuration Data**:
    
    -   Remember that your Firebase configuration data, especially the `apiKey`, should be handled securely.
    -   Avoid exposing these details in public repositories or unsecured files.


## Installation and Setup

1.  **Clone the Repository**:
    
    bashCopy code
    
    `git clone <repository_url>
    cd <repository_name>` 
    
2.  **Install Dependencies**:
    
    bashCopy code
    
    `pip install -r requirements.txt` 
    
3.  **Set Up Environment Variables**:
    
    -   Ensure the `.env` file is correctly configured with Firebase credentials.
4.  **Run the Application**:
    
    -   Start the FastAPI application using Uvicorn:
        
        bashCopy code
        
        `uvicorn api_queries:app --reload` 
        

## Running Tests

To verify that all endpoints are functioning as expected:

1.  **Execute Unit Tests**:
    
    bashCopy code
    
    `pytest unit_tests.py` 
    
2.  **Test Results**:
    
    -   Review the output of pytest to ensure all tests pass successfully.

## Usage

Once the microservice is up and running, the authenticated endpoints can be accessed and integrated into any user interface or system that requires data querying capabilities on the parquet dataset. 

**