import json
import random
from datetime import datetime, timedelta

# Define the start and end dates for the price history
start_date = datetime.now() - timedelta(days=365*3)
end_date = datetime.now()

# Define products (IDs should match your database entries)
products = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10
]

# Helper function to generate random price
def generate_price(base_price):
    return round(base_price + random.uniform(-0.5, 0.5), 2)

# Helper function to determine if a product is on sale
def is_on_sale():
    return random.choice([True, False])

# Create a list to hold all price history records
price_history = []

# Generate data for each product
for product_id in products:
    current_date = start_date
    while current_date <= end_date:
        price_history.append({
            "model": "market.pricehistory",
            "pk": len(price_history) + 1,
            "fields": {
                "product": product_id,
                "price": generate_price(random.uniform(1.99, 10.99)),
                "date": current_date.strftime('%Y-%m-%d'),
                "on_sale": is_on_sale()
            }
        })
        current_date += timedelta(days=1)

# Write the data to a JSON file
with open('pricehistory.json', 'w') as file:
    json.dump(price_history, file, indent=4)
