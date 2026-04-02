import requests
from bs4 import BeautifulSoup

def scrape_flipkart(search_query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    # Flipkart search URL
    url = f"https://www.flipkart.com/search?q={search_query}"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch Flipkart page")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    products = []

    # Flipkart has 2 main types of search result blocks
    results = soup.find_all("div", {"class": "_1AtVbE"})  # search result container

    for item in results[:10]:  # limit to 10 products for demo
        # Product name
        title_tag = item.find("a", {"class": "IRpwTa"})
        if not title_tag:
            title_tag = item.find("a", {"class": "s1Q9rs"})
        title = title_tag.text.strip() if title_tag else None

        # Price
        price_tag = item.find("div", {"class": "_30jeq3"})
        price = price_tag.text.replace("₹", "").replace(",", "").strip() if price_tag else None

        # Rating
        rating_tag = item.find("div", {"class": "_3LWZlK"})
        rating = rating_tag.text.strip() if rating_tag else None

        if title and price:
            products.append({
                "name": title[:60],  # short title for demo
                "price": float(price) if price else 0,
                "rating": float(rating) if rating else None,
                "platform": "Flipkart"
            })

    return products

# Test run
if __name__ == "__main__":
    data = scrape_flipkart("iphone")
    for p in data:
        print(p)