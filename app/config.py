import os
from dotenv import load_dotenv

dotenv_path = os.path.join('app/data', '.env')

load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')