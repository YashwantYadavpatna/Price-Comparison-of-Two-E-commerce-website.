#pip install requests beautifulsoup4 pandas matplotlib
import requests
from bs4 import BeautifulSoup
import pandas as pd   
def scrape_amazon(product):
    base_url = 'https://www.amazon.com'
    search_url = f'{base_url}/s?k={product.replace(" ", "+")}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract product information
        product_titles = [item.text.strip() for item in soup.find_all('span', class_='a-size-base-plus a-color-base a-text-normal')]
        product_prices = [item.text.strip() for item in soup.find_all('span', class_='a-price-whole')]
        # Create a dataframe with product titles and prices
        df = pd.DataFrame({'Title': product_titles, 'Price_Amazon': product_prices})
        return df
    else:
        print(f"Failed to fetch Amazon for {product}")
def scrape_flipkart(product):
    base_url = 'https://www.flipkart.com'
    search_url = f'{base_url}/search?q={product.replace(" ", "%20")}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract product information
        product_titles = [item.text.strip() for item in soup.find_all('div', class_='_4rR01T')]
        product_prices = [item.text.strip().replace('₹', '') for item in soup.find_all('div', class_='_30jeq3 _1_WHN1')]
        # Create a dataframe with product titles and prices
        df = pd.DataFrame({'Title': product_titles, 'Price_Flipkart': product_prices})
        return df
    else:
        print(f"Failed to fetch Flipkart for {product}")

# Specify the product to search for
product = 'iPhone 15'
# Scrape data from Amazon and Flipkart
data_amazon = scrape_amazon(product)
data_flipkart = scrape_flipkart(product)
if data_amazon is not None and data_flipkart is not None:
    # Display the scraped data
    print("Data from Amazon:")
    print(data_amazon.head())
    print("\nData from Flipkart:")
    print(data_flipkart.head())
    # Merge datasets based on product title (assuming titles are unique identifiers)
    merged_data = pd.merge(data_amazon, data_flipkart, on='Title', how='inner')
    # Print and visualize the comparison
    print("\nComparison of Prices for iPhone 15:")
    print(merged_data[['Title', 'Price_Amazon', 'Price_Flipkart']])

    # Visualization (example using matplotlib)
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    plt.scatter(merged_data['Price_Amazon'], merged_data['Price_Flipkart'])
    plt.xlabel('Price from Amazon')
    plt.ylabel('Price from Flipkart')
    plt.title('Comparison of Prices for iPhone 15')
    plt.grid(True)
    plt.show()
else:
    print("Failed to scrape data from one or both websites.")
#Step 3: Database Storage
#We'll use SQLite for demonstration purposes to store scraped data into two tables:
import sqlite3
# Connect to SQLite database (create if not exists)
conn = sqlite3.connect('ecommerce_data.db')
# Write data to SQLite tables
data1=data_amazon
data2=data_flipkart
data1.to_sql('Website1_Products', conn, if_exists='replace', index=False)
data2.to_sql('Website2_Products', conn, if_exists='replace', index=False)
# Commit changes and close connection
conn.commit()
conn.close()
print("Data saved to SQLite database.")