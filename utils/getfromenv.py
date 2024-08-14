from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Access variables

YOUR_CLIENT_ID = os.getenv("YOUR_CLIENT_ID")
YOUR_CLIENT_SECRET = os.getenv("YOUR_CLIENT_SECRET")
YOUR_APP_NAME = os.getenv("YOUR_APP")
