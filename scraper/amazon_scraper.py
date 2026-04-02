import requests
from bs4 import BeautifulSoup
import time

def scrape_amazon(search_query, max_retries=3, delay=2):
    """
    Scrape Amazon for a given search query.

    Args:
        search_query (str): The search keyword.
        max_retries (int): Number of retry attempts if request fails.
        delay (int): Seconds to wait between retries.

    Returns:
        List[dict]: List of products with name, price, rating, platform, and product URL.
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9"
    }

    url = f"https://www.amazon.in/s?k={search_query}"

    # Retry mechanism
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                break
            else:
                print(f"Attempt {attempt}: Failed to fetch page (status {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt}: Request failed ({e})")
        
        if attempt < max_retries:
            print(f"Retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            print("Max retries reached. Skipping this query.")
            return []

    soup = BeautifulSoup(response.text, "lxml")
    products = []

    results = soup.find_all("div", {"data-component-type": "s-search-result"})

    for item in results[:10]:  # limit to first 10 products for demo
        title_tag = item.find("span", class_="a-size-medium")
        title = title_tag.text.strip() if title_tag else None

        price_whole = item.find("span", "a-price-whole")
        price = price_whole.text.replace(",", "") if price_whole else None

        rating_tag = item.find("span", "a-icon-alt")
        rating = rating_tag.text.split()[0] if rating_tag else None

        link_tag = item.find("a", class_="a-link-normal s-no-outline")
        product_url = f"https://www.amazon.in{link_tag['href']}" if link_tag else None

        if title and price and product_url:
            products.append({
                "name": title[:60],  # truncate long names
                "price": float(price),
                "rating": float(rating) if rating else None,
                "platform": "Amazon",
                "url": product_url
            })

    return products

# Test run
if __name__ == "__main__":
    data = scrape_amazon("iphone")
    for product in data:
        print(product)