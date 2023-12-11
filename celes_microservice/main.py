import asyncio
import json
from firebase_auth import create_access_token, get_valid_token
import requests
import asyncio
import json


async def main():
    token_response = await get_valid_token()
    token = token_response['token'] 

    key = "1|17542"
    from_date = "2023-01-01"
    to_date = "2023-12-31" 

    url = f"http://127.0.0.1:8000/sales_per_employee/{key}?from_date={from_date}&to_date={to_date}"

    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        json_data = response.json()
        print(json_data)
    else:
        error_message = response.content.decode("utf-8") 
        print(f"Failed to fetch data. Status code: {response.status_code}. Error: {error_message}")
    

if __name__ == "__main__":
    asyncio.run(main())
