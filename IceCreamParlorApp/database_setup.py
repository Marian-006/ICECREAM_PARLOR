import sqlite3

def initialize_db():
    connection = sqlite3.connect("ice_cream_parlor.db")
    cursor = connection.cursor()

    # Seasonal Flavors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flavors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        is_seasonal INTEGER DEFAULT 1
    )
    """)

    # Ingredient Inventory Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )
    """)

    # Allergens Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS allergens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    )
    """)

    # Customer Suggestions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavor_name TEXT NOT NULL,
        customer_name TEXT,
        allergies TEXT
    )
    """)

    # Cart Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL
    )
    """)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_db()
    print("Database initialized successfully!")
