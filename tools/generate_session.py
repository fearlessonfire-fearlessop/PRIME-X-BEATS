from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()
api_id=int(os.environ["API_ID"])
api_hash=os.environ["API_HASH"]

print("Telegram assistant session generator")
print("Your phone/login code is entered directly into this terminal.")
with Client("prime_assistant_generator", api_id=api_id, api_hash=api_hash, in_memory=True) as app:
    print("\nASSISTANT_SESSION=" + app.export_session_string())
  
