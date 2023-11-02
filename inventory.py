import csv
import json
from datetime import date
from main import inventory_log_headers

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
        # Load existing inventory items from the data file
        items = []
        with open(self.inventory_data, "r") as file:
            items = json.load(file)

        # Iterate through the inventory items to find the specified item by name
        for item in items:
            if item["name"] == name:
                # Check if the available quantity in inventory is sufficient for the transfer
                if item["qty"] >= quantity:
                    # Reduce the quantity of the item in inventory by the transferred amount
                    item["qty"] -= quantity
                    price = item["price"]  # Get the price of the item for logging purposes
                    break
                else:
                    # If there is not enough quantity in inventory, print an error message and return False
                    print("[INVENTORY] {name} is {qty} units less than required amount".format(name=name, qty=quantity-item["qty"]))
                    return False

        # Update the inventory data file with the modified item quantities
        with open(self.inventory_data, "w") as file:
            json.dump(items, file)

        # Log the transfer operation in the inventory log file
        with open(self.inventory_log, "a") as file:
            csv.DictWriter(file, fieldnames=inventory_log_headers, delimiter=';').writerow(
                {"date": date.today(), "item": name, "product": product, "qty": quantity, "cost": price})

        # Print a success message indicating the transfer of items to production and return True
        print("[INVENTORY] Transferred {qty} units of {item} to product {product}".format(qty=quantity, item=name, product=product))
        return True