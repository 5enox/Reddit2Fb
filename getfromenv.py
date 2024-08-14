import dotenv
import os

dotenv.load_dotenv()

YOUR_CLIENT_ID = os.getenv('YOUR_CLIENT_ID')
YOUR_CLIENT_SECRET = os.getenv('YOUR_CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')
FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN')
