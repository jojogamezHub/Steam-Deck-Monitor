import requests
import time
import os
from discord_webhook import DiscordWebhook

# --- CONFIGURATION ---
COUNTRY_CODE = 'CA'  # Canada
WEBHOOK_URL = 'https://discordapp.com/api/webhooks/1271948927826133090/chv1Noy-9AUNsDkToH7xkVbyu4XSogwuFFRan03QIgH7Mc8jcnlviAGTyMeAG2BQ2Sev' # Replace this!

# Model Name -> Package ID mapping (Fixed syntax errors in strings)
MODELS = {
    "256GB Steam Deck": "539246",
    "512GB Steam Deck": "595605",
    "256GB Cert Refurbed Deck": "903906",
    "Steam Controller": "1558609",
    "Steam Machine": "4165910"
}

API_URL = "https://api.steampowered.com/IPhysicalGoodsService/CheckInventoryAvailableByPackage/v1/"

def check_stock():
    for name, package_id in MODELS.items():
        params = {
            'origin': 'https://store.steampowered.com',
            'country_code': COUNTRY_CODE,
            'packageid': package_id
        }
        
        headers = {'User-Agent': 'Mozilla/5.0'}

        try:
            response = requests.get(API_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            is_available = data.get("response", {}).get("inventory_available", False)
            current_status = "INSTOCK" if is_available else "OUTOFSTOCK"
            
            filename = f"status_{package_id}.txt"
            old_status = ""
            
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    old_status = f.read().strip()

            if current_status != old_status:
                print(f"Update for {name}: {current_status}")
                
                with open(filename, "w") as f:
                    f.write(current_status)
                
                # --- TIMESTAMP LOGIC ---
                # Get current unix timestamp
                now = int(time.time())
                discord_time = f"<t:{now}:F>" # Full date/time format
                
                # Send to Discord
                msg = (
                    f"🚨 **Stock Update!**\n"
                    f"**Model:** {name}\n"
                    f"**Status:** {'✅ Available' if is_available else '❌ Out of Stock'}\n"
                    f"**Checked at:** {discord_time}"
                )
                
                webhook = DiscordWebhook(url=WEBHOOK_URL, content=msg)
                webhook.execute()
            else:
                print(f"No change for {name} ({current_status})")

        except Exception as e:
            print(f"Error checking {name}: {e}")

# --- EXECUTION ---
if __name__ == "__main__":
    check_stock()
