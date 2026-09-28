import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("API_KEY")
if not token:
    raise ValueError("API_KEY environment variable is not set.")
else:
    print(token)