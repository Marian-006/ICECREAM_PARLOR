import sqlite3
from tabulate import tabulate

DB_PATH = "ice_cream_parlor.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

# Add a seasonal flavor
def add_flavor():
    name = input("Enter flavor name: ")
    description = input("Enter flavor description: ")
    is_seasonal = input("Is it seasonal? (1 for Yes, 0 for No): ")
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO flavors (name, description, is_seasonal)
    VALUES (?, ?, ?)
    """, (name, description, is_seasonal))
    conn.commit()
    conn.close()
    print(f"Flavor '{name}' added successfully.")

# View all flavors with search and filter options
def view_flavors():
    search = input("Search by name (leave blank to view all): ").strip()
    is_seasonal = input("Filter by seasonal flavors? (1 for Yes, 0 for No, leave blank for all): ").strip()

    conn = connect_db()
    cursor = conn.cursor()

    query = "SELECT id, name, description, is_seasonal FROM flavors WHERE 1=1"
    params = []
    if search:
        query += " AND name LIKE ?"
        params.append(f"%{search}%")
    if is_seasonal:
        query += " AND is_seasonal = ?"
        params.append(is_seasonal)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print(tabulate(rows, headers=["ID", "Name", "Description", "Seasonal"]))
    else:
        print("No flavors found.")

# Add allergens
def add_allergen():
    allergen = input("Enter allergen name: ")
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO allergens (name) VALUES (?)", (allergen,))
        conn.commit()
        print(f"Allergen '{allergen}' added successfully.")
    except sqlite3.IntegrityError:
        print("Allergen already exists.")
    finally:
        conn.close()

# Manage the cart
def view_cart():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, product_name FROM cart")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print(tabulate(rows, headers=["ID", "Product Name"]))
    else:
        print("Your cart is empty.")

def add_to_cart():
    product_name = input("Enter product name to add to cart: ")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO cart (product_name) VALUES (?)", (product_name,))
    conn.commit()
    conn.close()
    print(f"'{product_name}' added to cart.")

def main_menu():
    while True:
        print("\nIce Cream Parlor Cafe")
        print("1. Add Seasonal Flavor")
        print("2. View Flavors")
        print("3. Add Allergen")
        print("4. View Cart")
        print("5. Add to Cart")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_flavor()
        elif choice == "2":
            view_flavors()
        elif choice == "3":
            add_allergen()
        elif choice == "4":
            view_cart()
        elif choice == "5":
            add_to_cart()
        elif choice == "6":
            print("Thank you for using the Ice Cream Parlor Cafe app!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
