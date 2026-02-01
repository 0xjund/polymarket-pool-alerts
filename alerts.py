import os
import requests
from dotenv import load_dotenv

# Load bot token
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT')

def send_telegram_alert(message: str) -> bool:
    """Send an alert to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            print("✓ Alert sent to Telegram")
            return True
        else:
            print(f"✗ Failed to send alert: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Error sending Telegram message: {e}")
        return False

if __name__ == "__main__":
    # Test the alert
     #   test_message = """
#📈 TEST ALERT
#This is a test from your Polymarket bot!
#"""
    send_telegram_alert()
