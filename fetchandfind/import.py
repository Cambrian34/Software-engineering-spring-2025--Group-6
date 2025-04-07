import sqlite3
import csv
import sys
import os

DB_PATH = "db.sqlite3"  # Path to SQLite database
TABLE_NAME = "store_product"  # Replace with your actual table name

def import_products(csv_filepath):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(csv_filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            title = row["Title"]
            price = float(row["Price"].replace("$", "").strip())  # Convert price to float
            image_name = row["Image Name"]

            # Ensure image path starts with 'product_images/'
            image_path =  f"product_images/{image_name}"

            # Insert data into SQLite database
            cursor.execute(f"""
                INSERT INTO {TABLE_NAME} (name, description, price, stock_quantity, image, is_on_sale, sale_price, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, datetime('now'))
            """, (title, "Imported from CSV", price, 10, image_path, 0, None))

            print(f"Added: {title} - ${price} - {image_path}")

    conn.commit()
    conn.close()
    print("Import complete!")

if __name__ == "__main__":

    csv_filepath = "/Users/alistairchambers/Downloads/Amazon scaper/amazon_products.csv"
    if not os.path.exists(csv_filepath):
        print("Error: CSV file not found.")
        sys.exit(1)

    import_products(csv_filepath)