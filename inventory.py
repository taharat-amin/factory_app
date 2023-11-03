import csv
import json
from datetime import date
from os import system

inventory_log_headers = ["date", "item", "product", "qty", "cost"]


class Inventory:
    # Class variable to store the path of the inventory data file
    inventory_data = ".json/inventory.json"
    inventory_log = ".csv/inventory_log.csv"

    # Constructor method to initialize the Inventory object
    def __init__(self, main_screen_init=False):
        if main_screen_init:
            print("[INVENTORY] Inventory counted...\n")

    # Representation method to provide a string representation of the class
    def __repr__(self):
        text = ''
        items = []
        with open(self.inventory_data, "r") as file:
            try:
                items = json.load(file)
            except json.decoder.JSONDecodeError:
                print("\033[91m\n[INVENTORY]  \033[0m", end='')
                return "[INVENTORY] No item exists in inventory\n"

        longest_name = len("Name")
        longest_quantity = len("Quantity")
        longest_price = len("Price")
        for item in items:
            if len(item["name"]) > longest_name:
                longest_name = len(item["name"])
            if len(str(item["qty"])) > longest_quantity:
                longest_quantity = len(str(item["qty"]))
            if len(str(item["price"])) > longest_price:
                longest_price = len(str(item["price"]))

        text += "Inventory".center(longest_name +
                                   longest_quantity+longest_price+8)+"\n"
        text += "-"*(longest_name+longest_quantity+longest_price+8)+"\n"
        text += "Item"+" " * \
            (longest_name-len("Item"))+" | "
        text += "Quantity" + \
            " "*(longest_quantity-len("Quantity"))+" | "
        text += "Price"+" " * \
            (longest_price-len("Price"))+" |\n"
        text += "-"*(longest_name+1)+"+"+"-" * \
            (longest_quantity+2)+"+"+"-"*(longest_price+3)+"\n"

        for item in items:

            text += "{name} | {qty} | {price} |\n".format(
                name=item["name"].ljust(longest_name),
                qty=str(
                    item["qty"]).rjust(longest_quantity),
                price=str(item["price"]).rjust(longest_price)
            )

        text += "-"*(longest_name+longest_quantity+longest_price+8)+"\n"

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
                print("\033[93m\n[INVENTORY] \033[0m", end='')
                print("\nAdded {qty} units of {item} @ Tk.{price}/unit\n".format(
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
            print("\033[93m\n[INVENTORY] \033[0m", end='')
            print("Added {qty} units of {item} @ Tk.{price}/unit\n".format(
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
                    # Get the price of the item for logging purposes
                    price = item["price"]
                    price *= quantity
                    break
                else:
                    # If there is not enough quantity in inventory, print an error message and return False
                    print("\033[91m\n[INVENTORY] \033[0m", end='')
                    print("{name} is {qty} units less than required amount\n".format(
                        name=name, qty=quantity-item["qty"]))
                    return False, 0
        else:
            print("\033[91m\n[INVENTORY] \033[0m", end='')
            print("{name} not available in inventory\n")
            return False, 0

        # Update the inventory data file with the modified item quantities
        with open(self.inventory_data, "w") as file:
            json.dump(items, file)

        # Log the transfer operation in the inventory log file
        with open(self.inventory_log, "a") as file:
            csv.DictWriter(file, fieldnames=inventory_log_headers, delimiter=';').writerow(
                {"date": date.today(), "item": name, "product": product, "qty": quantity, "cost": price})

        # Print a success message indicating the transfer of items to production and return price of the item for product cost calculation
        print("\033[92m\n[INVENTORY] \033[0m", end='')
        print("[INVENTORY] Transferred {qty} units of {item} to produce {product}\n".format(
            qty=quantity, item=name, product=product))
        return True, price

    # Generate log report
    def generate_report(self):
        system("cp .csv/inventory_log.csv \"Inventory Log Report\".csv")
        print("\033[93m\n[INVENTORY] \033[0m", end='')
        print("Generated inventory log report\n")
