import requests


def get_crypto_data():
    try:
        # 🔹 1. Trending coins
        trending_url = "https://api.coingecko.com/api/v3/search/trending"
        trending_data = requests.get(trending_url).json()
        coins = trending_data.get("coins", [])

        trending_list = []
        for coin in coins[:5]:
            item = coin.get("item", {})
            name = item.get("name", "Unknown")
            symbol = item.get("symbol", "")
            trending_list.append(f"{name} ({symbol})")

        # 🔹 2. Market data (top coins)
        market_url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=5&page=1"
        market_data = requests.get(market_url).json()

        market_list = []
        for coin in market_data:
            name = coin.get("name")
            price = coin.get("current_price")
            change = coin.get("price_change_percentage_24h")

            market_list.append(f"{name}: ${price} ({change:.2f}% 24h)")

        return {
            "trending": trending_list,
            "market": market_list
        }

    except Exception as e:
        return {"error": str(e)}
