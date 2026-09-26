import validators
import requests
from fastapi import HTTPException


def validate_url(target_url: str) -> str:
    # 1. Validate the URL format first to prevent network crashes
    if not validators.url(target_url):
        raise HTTPException(status_code=400, detail="The site URL format is incorrect or illegal")

    # 2. Check if the website is live and active
    try:
        # Added a timeout to stop slow sites from freezing your server
        response = requests.get(target_url, timeout=5.0)
        
        if response.status_code == 200:
            print('Site works and is available')
            return target_url
        else:
            raise HTTPException(status_code=404, detail="Site is not active...")
            
    except requests.exceptions.RequestException:
        # Catches bad domains, connection drops, and timeout errors safely
        raise HTTPException(status_code=404, detail="Site is completely unreachable...")
