import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5'
}

def get_product_details(product_url: str) -> dict:
    product_details = {}
    
    try:
        # Get the product page content and create a BeautifulSoup object
        page = requests.get(product_url, headers=headers)
        page.raise_for_status()  # Raise HTTPError for bad responses
        soup = BeautifulSoup(page.content, features="lxml")
        
        # Scrape the product details
        title = soup.find("span", attrs={"id": "productTitle"})
        price_element = soup.find("span", attrs={"class": "a-price"})
        
        if title:
            product_details["title"] = title.get_text().strip()
        else:
            product_details["title"] = "Title not found"
        
        if price_element:
            extracted_price = price_element.get_text().strip()
            
            if "$" in extracted_price:
                price = "$" + extracted_price.split("$")[1]
            else:
                price = extracted_price
            product_details["price"] = price
        else:
            product_details["price"] = "Price not found"
        
    except requests.RequestException as e:
        print("Could not fetch product details")
        print(f"Failed with exception: {e}")
    except Exception as e:
        print("An error occurred")
        print(f"Failed with exception: {e}")
    
    return product_details

# Example usage:
product_url = input("Enter product url: ")
product_details = get_product_details(product_url)
print(product_details)
