from os.path import exists
from os import system
import csv
import json

# Placed in global scope because of use in multiple place of the code
csv_headers = ["date", "product", "employee", "cost"]

class Inventory:
    # Class variable to store the path of the inventory data file
    inventory_data = 'inventory.json'

    # Constructor method to initialize the Inventory object
    def __init__(self):
        print("[INVENTORY] Inventory object initiated...")

    # Representation method to provide a string representation of the class
    def __repr__(self):
        return """This class manages raw material inventory of the factory\nInventory class data heads:\n\"name\": The name of the item\n\"qty\": The quantity of the item\n\"price\": The moving average price per unit of the item"""

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
                json.dump([{"name": name, "qty": quantity, "price": new_price}], file)
                print("[SUCCESS] Added {qty} units of {item} @ Tk.{price}/unit".format(
                    qty=quantity, item=name, price=new_price))
                return

        # Iterate through the existing items in the inventory
        for item in items:
            # If the item already exists in the inventory, update its quantity and price
            if item["name"] == name:
                price = item["qty"] * item["price"]  # Calculate total cost of existing items
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
            json.dump(items, file)  # Serialize items list to JSON and write to file
            print("[SUCCESS] Added {qty} units of {item} @ Tk.{price}/unit".format(
                qty=quantity, item=name, price=new_price))
        return


class Employee:

    employee_data = '.employees.json'

    def __init__(self) -> None:

        print("[EMPLOYEE] Employee object initiated...")

    def __repr__(self):

        return "This class manages employees of the factory"


class Product:

    product_data = '.products.json'
    finished_goods_data = '.finished_goods.csv'

    def __init__(self) -> None:

        print("[PRODUCT] Product object initiated...")

    def __repr__(self) -> str:

        return "This class manages finished goods inventory of the factory"

#Create the data files if those does not exist
if not exists("inventory.json"):
    system("touch .inventory.json")
if not exists("employees.json"):
    system("touch .employees.json")
if not exists("products.json"):
    system("touch .products.json")
if not exists("finished_goods.csv"):
    system("touch .finished_goods.csv")
    with open(".finished_goods.csv", "w") as file:
        csv.DictWriter(file, fieldnames=csv_headers,
                       delimiter=';').writeheader()

print("[SYSTEM] Initiating system...")
print("[DATA] Data storage initiated...")
inv = Inventory()
emp = Employee()
pro = Product()
print("[SYSTEM] System initiated...")
print("------FACTORY MANAGEMENT SYSTEM------")
inv.add_item("Copper", 16, 2.5)
inv.add_item("Iron", 20, 10)