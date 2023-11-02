from os.path import exists
from os import system
import csv
import json
from datetime import date

# Placed in global scope because of use in multiple place of the code
product_headers = ["date", "product", "employee", "cost"]
inventory_log_headers = ["date", "item", "product", "qty", "cost"]


class Inventory:
    # Class variable to store the path of the inventory data file
    inventory_data = ".json/inventory.json"
    inventory_log = ".csv/inventory_log.csv"

    # Constructor method to initialize the Inventory object
    def __init__(self):
        print("[INVENTORY] Inventory object initialized...")

    # Representation method to provide a string representation of the class
    def __repr__(self):
        text = ""
        items = []
        with open(self.inventory_data, "r") as file:
            try:
                items = json.load(file)
            except json.decoder.JSONDecodeError:
                return "[INVENTORY] No item exists in inventory"

        for item in items:
            text += str(item)+"\n"

        return text

    # Method to add items to the inventory
    def add_item(self, name, quantity, new_price):
        items = []  # List to store all inventory items

        # Try to open the inventory data file
        with open(self.inventory_data, "r+") as file:
            try:
                # Attempt to load data from the file
                items = json.load(file)
            except:
                # If the file is empty, add the new item directly to the file
                json.dump(
                    [{"name": name, "qty": quantity, "price": new_price}], file)
                print("[INVENTORY] Added {qty} units of {item} @ Tk.{price}/unit".format(
                    qty=quantity, item=name, price=new_price))
                return

        # Iterate through the existing items in the inventory
        for item in items:
            # If the item already exists in the inventory, update its quantity and price
            if item["name"] == name:
                # Calculate total cost of existing items
                price = item["qty"] * item["price"]
                item["qty"] += quantity  # Update quantity
                price += quantity * new_price  # Add cost of new items
                price /= item["qty"]  # Calculate new average price
                item["price"] = price  # Update average price
                break
        else:
            # If the item is not found in the inventory, add it to the items list
            items.append({"name": name, "qty": quantity, "price": new_price})

        # Write the updated inventory data back to the file
        with open(self.inventory_data, "w") as file:
            # Serialize items list to JSON and write to file
            json.dump(items, file)
            print("[INVENTORY] Added {qty} units of {item} @ Tk.{price}/unit".format(
                qty=quantity, item=name, price=new_price))
        return

    # Method to transfer raw material to production
    def transfer_to_production(self, name, product, quantity):

        items = []
        price = 0
        with open(self.inventory_data, "r") as file:
            items = json.load(file)

        for item in items:
            if item["name"] == name:
                item["qty"] -= quantity
                price = item["price"]
                break

        with open(self.inventory_data, "w") as file:
            json.dump(items, file)

        with open(self.inventory_log, "a") as file:
            csv.DictWriter(file, fieldnames=inventory_log_headers, delimiter=';').writerow(
                {"date": date.today(), "item": name, "product": product, "qty": quantity, "cost": price})
            
        print("[INVENTORY] Transferred {qty} units of {item} to product {product}".format(qty=quantity, item=name, product=product))


class Employee:

    employee_data = '.employees.json'

    def __init__(self) -> None:

        print("[EMPLOYEE] Employee object initialized...")

    def __repr__(self):

        return "This class manages employees of the factory"


class Product:

    product_data = '.products.json'
    finished_goods_data = '.finished_goods.csv'

    def __init__(self) -> None:

        print("[PRODUCT] Product object initialized...")

    def __repr__(self) -> str:

        return "This class manages finished goods inventory of the factory"

# Create folders for better management
if not exists("./.json"):
    system("mkdir .json")

if not exists("./.csv"):
    system("mkdir .csv")

# Create the data files if those does not exist
if not exists(".json/inventory.json"):
    system("touch .json/inventory.json")

if not exists(".csv/inventory_log.csv"):
    system("touch .csv/inventory_log.csv")
    with open(".csv/inventory_log.csv", "w") as file:
        csv.DictWriter(file, fieldnames=inventory_log_headers,
                       delimiter=';').writeheader()
        
if not exists(".json/employees.json"):
    system("touch .json/employees.json")

if not exists(".json/products.json"):
    system("touch .json/products.json")

if not exists(".csv/finished_goods.csv"):
    system("touch .csv/finished_goods.csv")
    with open(".csv/finished_goods.csv", "w") as file:
        csv.DictWriter(file, fieldnames=product_headers,
                       delimiter=';').writeheader()

print("[SYSTEM] Initializing system...")
print("[DATA] Data storage initialized...")
inv = Inventory()
emp = Employee()
pro = Product()
print("[SYSTEM] System initialized...")

print("""\n
███████╗ █████╗  ██████╗████████╗ ██████╗ ██████╗ ██╗   ██╗    ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗███╗   ███╗███████╗███╗   ██╗████████╗    ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
██╔════╝██╔══██╗██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝    ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝████╗ ████║██╔════╝████╗  ██║╚══██╔══╝    ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
█████╗  ███████║██║        ██║   ██║   ██║██████╔╝ ╚████╔╝     ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██╔████╔██║█████╗  ██╔██╗ ██║   ██║       ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
██╔══╝  ██╔══██║██║        ██║   ██║   ██║██╔══██╗  ╚██╔╝      ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║   ██║██╔══╝  ██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║       ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
██║     ██║  ██║╚██████╗   ██║   ╚██████╔╝██║  ██║   ██║       ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║ ╚═╝ ██║███████╗██║ ╚████║   ██║       ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝ ╚═════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝       ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
                                                                                                                                                                                                                    \n""")
inv.add_item("Copper", 16, 2.5)
inv.add_item("Iron", 20, 10)
inv.transfer_to_production("Copper", "Cables", 6)
