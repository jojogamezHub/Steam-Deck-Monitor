import requests
import time
import os
from discord_webhook import DiscordWebhook

# --- CONFIGURATION ---
COUNTRY_CODE = 'CA'  # Canada
WEBHOOK_URL = 'YOUR_NEW_WEBHOOK_URL' # Replace this!

# Model Name -> Package ID mapping (Refurbished Units)
MODELS = {
    "64GB Refurb": "903905",
    "256GB Refurb": "903906",
    "512GB Refurb": "903907"
}

API_URL = "https://api.steampowered.com/IPhysicalGoodsService/CheckInventoryAvailableByPackage/v1/"

def check_stock():
    for name, package_id in MODELS.items():
        params = {
            'origin': 'https://store.steampowered.com',
            'country_code': COUNTRY_CODE,
            'packageid': package_id
        }
        
        # Steam API sometimes requires a basic User-Agent to avoid 400 errors
        headers = {'User-Agent': 'Mozilla/5.0'}

        try:
            response = requests.get(API_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # The API returns True or False
            is_available = data.get("response", {}).get("inventory_available", False)
            current_status = "INSTOCK" if is_available else "OUTOFSTOCK"
            
            # Check for changes using a local file
            filename = f"status_{package_id}.txt"
            old_status = ""
            
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    old_status = f.read().strip()

            # If the status changed, send a notification
            if current_status != old_status:
                print(f"Update for {name}: {current_status}")
                
                # Update the file
                with open(filename, "w") as f:
                    f.write(current_status)
                
                # Send to Discord
                msg = f"🚨 **Stock Update!**\nModel: {name}\nStatus: {'✅ Available' if is_available else '❌ Out of Stock'}"
                webhook = DiscordWebhook(url=WEBHOOK_URL, content=msg)
                webhook.execute()
            else:
                print(f"No change for {name} ({current_status})")

        except Exception as e:
            print(f"Error checking {name}: {e}")

 check_stock()
