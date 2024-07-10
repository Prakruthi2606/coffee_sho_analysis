import pymysql
import mysql.connector

class ProductManagement:
    def _init_(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="himysql@987",
            database="coffee_shop"
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255) NOT NULL,
                                price DECIMAL(10, 2) NOT NULL,
                                quantity INT NOT NULL
                            )''')
        self.connection.commit()

    def add_product(self, name, price, quantity):
        self.cursor.execute('''INSERT INTO products (name, price, quantity) 
                            VALUES (%s, %s, %s)''', (name, price, quantity))
        self.connection.commit()

    def get_product(self, product_id):
        self.cursor.execute('''SELECT * FROM products WHERE id=%s''', (product_id,))
        return self.cursor.fetchone()

    def update_product(self, product_id, name=None, price=None, quantity=None):
        update_query = "UPDATE products SET"
        update_params = []

        if name:
            update_query += " name=%s,"
            update_params.append(name)
        if price:
            update_query += " price=%s,"
            update_params.append(price)
        if quantity:
            update_query += " quantity=%s,"
            update_params.append(quantity)

        # Remove the trailing comma
        update_query = update_query.rstrip(',')

        # Add product_id to the params list
        update_params.append(product_id)

        # Execute the update query
        self.cursor.execute(update_query + " WHERE id=%s", update_params)
        self.connection.commit()

    def delete_product(self, product_id):
        self.cursor.execute('''DELETE FROM products WHERE id=%s''', (product_id,))
        self.connection.commit()

    def get_all_products(self):
        self.cursor.execute('''SELECT * FROM products''')
        return self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

def display_products(products):
    print("%-5s %-20s %-10s %-10s" % ("ID", "Name", "Price ($)", "Quantity"))
    for product in products:
        print("%-5s %-20s %-10s %-10s" % product)

def main():
    product_mgmt = ProductManagement()

    while True:
        print("\n1: Add Product\n2: Get Product\n3: Update Product\n4: Delete Product\n5: View All Products\n6: Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter product quantity: "))
            product_mgmt.add_product(name, price, quantity)
            print("Product added successfully.")

        elif choice == '2':
            product_id = int(input("Enter product ID: "))
            product = product_mgmt.get_product(product_id)
            if product:
                print("Product found:")
                print("ID: {}, Name: {}, Price: {}, Quantity: {}".format(*product))
            else:
                print("Product not found.")

        elif choice == '3':
            product_id = int(input("Enter product ID: "))
            name = input("Enter updated product name (leave blank to keep current): ")
            price = float(input("Enter updated product price (leave blank to keep current): ")) if input else None
            quantity = int(input("Enter updated product quantity (leave blank to keep current): ")) if input else None
            product_mgmt.update_product(product_id, name, price, quantity)
            print("Product updated successfully.")

        elif choice == '4':
            product_id = int(input("Enter product ID to delete: "))
            product_mgmt.delete_product(product_id)
            print("Product deleted successfully.")

        elif choice == '5':
            products = product_mgmt.get_all_products()
            if products:
                print("All products:")
                display_products(products)
            else:
                print("No products found.")

        elif choice == '6':
            product_mgmt.close_connection()
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if _name_ == "_main_":
    main()