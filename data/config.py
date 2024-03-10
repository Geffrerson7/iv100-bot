import os
from dotenv import load_dotenv


load_dotenv()

token = os.environ.get("TOKEN")
developer_chat_id = os.environ.get("DEVELOPER_CHAT_ID")