import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Button, Style

DB_PATH = "ice_cream_parlor.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

# GUI Functions
def add_flavor():
    def submit():
        name = name_entry.get()
        description = desc_entry.get()
        is_seasonal = seasonal_var.get()
        
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO flavors (name, description, is_seasonal)
        VALUES (?, ?, ?)
        """, (name, description, is_seasonal))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Flavor '{name}' added successfully!")
        add_window.destroy()

    add_window = Toplevel(root)
    add_window.title("Add Flavor")
    add_window.geometry("400x300")
    add_window.configure(bg="#f0f0f0")

    Label(add_window, text="Add New Flavor", font=("Arial", 18), bg="#f0f0f0").pack(pady=20)

    frame = Frame(add_window, bg="#f0f0f0", padx=10, pady=10)
    frame.pack(padx=20, pady=20, fill="both")

    Label(frame, text="Name", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    name_entry = Entry(frame, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    Label(frame, text="Description", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=10, sticky="w")
    desc_entry = Entry(frame, width=30)
    desc_entry.grid(row=1, column=1, padx=10, pady=10)

    Label(frame, text="Seasonal", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=10, sticky="w")
    seasonal_var = IntVar()
    Checkbutton(frame, variable=seasonal_var, bg="#f0f0f0").grid(row=2, column=1, padx=10, pady=10, sticky="w")

    Button(add_window, text="Submit", command=submit, style="Accent.TButton").pack(pady=10)

def view_flavors():
    def load_data():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, is_seasonal FROM flavors")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            tree.insert("", "end", values=row)

    view_window = Toplevel(root)
    view_window.title("View Flavors")
    view_window.geometry("600x400")
    view_window.configure(bg="#f0f0f0")

    tree = Treeview(view_window, columns=("ID", "Name", "Description", "Seasonal"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Description", text="Description")
    tree.heading("Seasonal", text="Seasonal")
    tree.pack(fill=BOTH, expand=True)

    load_data()

def add_allergen():
    def submit():
        allergen = allergen_entry.get()
        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO allergens (name) VALUES (?)", (allergen,))
            conn.commit()
            messagebox.showinfo("Success", f"Allergen '{allergen}' added successfully!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Allergen already exists.")
        finally:
            conn.close()
            add_window.destroy()
    
    add_window = Toplevel(root)
    add_window.title("Add Allergen")
    add_window.geometry("400x200")
    add_window.configure(bg="#f0f0f0")

    Label(add_window, text="Add New Allergen", font=("Arial", 16), bg="#f0f0f0").pack(pady=20)

    frame = Frame(add_window, bg="#f0f0f0", padx=10, pady=10)
    frame.pack(padx=20, pady=20, fill="both")

    Label(frame, text="Allergen Name", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    allergen_entry = Entry(frame, width=30)
    allergen_entry.grid(row=0, column=1, padx=10, pady=10)

    Button(add_window, text="Submit", command=submit, style="Accent.TButton").pack(pady=10)

def view_cart():
    def load_cart():
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, product_name FROM cart")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            tree.insert("", "end", values=row)

    cart_window = Toplevel(root)
    cart_window.title("View Cart")
    cart_window.geometry("400x300")
    cart_window.configure(bg="#f0f0f0")

    tree = Treeview(cart_window, columns=("ID", "Product Name"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Product Name", text="Product Name")
    tree.pack(fill=BOTH, expand=True)

    load_cart()

def add_to_cart():
    def submit():
        product_name = product_entry.get()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cart (product_name) VALUES (?)", (product_name,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"'{product_name}' added to cart!")
        add_window.destroy()

    add_window = Toplevel(root)
    add_window.title("Add to Cart")
    add_window.geometry("400x200")
    add_window.configure(bg="#f0f0f0")

    Label(add_window, text="Product Name", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=10, sticky="w")
    product_entry = Entry(add_window, width=30)
    product_entry.grid(row=0, column=1, padx=10, pady=10)

    Button(add_window, text="Submit", command=submit, style="Accent.TButton").grid(row=1, column=0, columnspan=2, pady=10)

# Main Application
root = Tk()
root.title("Ice Cream Parlor Cafe")
root.geometry("500x600")
root.configure(bg="#f0f0f0")

# Style Configurations
style = Style()
style.theme_use("clam")
style.configure("TButton", font=("Arial", 12), padding=5)
style.configure("Accent.TButton", font=("Arial", 12), padding=5, foreground="white", background="#0078D7")
style.configure("TLabel", font=("Arial", 14), background="#f0f0f0")

# Header Label
Label(root, text="Ice Cream Parlor Cafe", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)

# Buttons
Button(root, text="Add Flavor", command=add_flavor, style="TButton").pack(pady=10, fill="x", padx=50)
Button(root, text="View Flavors", command=view_flavors, style="TButton").pack(pady=10, fill="x", padx=50)
Button(root, text="Add Allergen", command=add_allergen, style="TButton").pack(pady=10, fill="x", padx=50)
Button(root, text="View Cart", command=view_cart, style="TButton").pack(pady=10, fill="x", padx=50)
Button(root, text="Add to Cart", command=add_to_cart, style="TButton").pack(pady=10, fill="x", padx=50)

root.mainloop()
