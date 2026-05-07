import requests
import os
from time import gmtime, strftime
from discord_webhook import DiscordWebhook

def superduperscraper(version, package_id):
    country_code = 'CA'
    # Using params dict is cleaner than string concatenation
    api_url = 'https://api.steampowered.com/IPhysicalGoodsService/CheckInventoryAvailableByPackage/v1/'
    params = {
        'origin': 'https://store.steampowered.com',
        'country_code': country_code,
        'packageid': package_id
    }
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    filename = f"{version}gb.txt"
    old_value = ""

    if os.path.isfile(filename):
        with open(filename, "r") as f:
            old_value = f.read().strip()

    try:
        r = requests.get(api_url, params=params, headers=headers)
        r.raise_for_status() # This will catch 400/500 errors
        
        data = r.json()
        # Navigate the JSON carefully
        availability = str(data.get("response", {}).get("inventory_available", "False"))
        
        print(f"{strftime('%Y-%m-%d %H:%M:%S', gmtime())} >> {version}GB: {availability}")

        with open(filename, "w") as f:
            f.write(availability)

        if old_value != "" and old_value != availability:
            status_msg = "available" if availability == "True" else "NOT available"
            webhook = DiscordWebhook(url="YOUR_WEBHOOK_URL", 
                                    content=f"Refurbished {version}GB Steam Deck is now {status_msg}!")
            webhook.execute()

    except Exception as e:
        print(f"Error checking {version}GB: {e}")

# Run checks
superduperscraper("64", "903905")
