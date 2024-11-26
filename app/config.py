import os
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(base_dir, 'data', '.env')

load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv('BOT_TOKEN')