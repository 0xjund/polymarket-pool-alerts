import requests

def fetch_all_markets(limit = 100, closed=None, order="desc"):
    """Fetch markets from Gamma API"""
    url = "https://gamma-api.polymarket.com/events"

    all_markets = []
    offset = 0

    while len(all_markets) < limit:
        params = {
            "limit": 100,
            "offset": offset,
            "closed": "false",
            "open": "true", 
        }

        if closed is not None:
            params["closed"] = closed
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        if not data:
            break 

        all_markets.extend(data)
        offset += 100

        print(f"Fetched {len(all_markets)} markets so far...")

        #Debug
        if len(all_markets) > 0:
            print(f"Sample creation date: {all_markets[-1].get('creationDate', 'N/A')}")

    return all_markets


