# Import required modules
from inventory import Inventory
from employee import Employee
from datetime import date
from os import system
import json
import csv

# Define headers for the product log CSV file
product_log_headers = ["date", "product", "quantity",
                       "material_cost", "labor_cost", "overhead_cost", "total_cost"]

# Initialize Inventory and Employee objects
inv = Inventory()
emp = Employee()

# Product class definition


class Product:
    # File paths for product data and product log
    product_data = '.json/products.json'
    product_log = '.csv/product_log.csv'

    # Constructor to initialize the Product object
    def __init__(self) -> None:
        print("[PRODUCT] Product object initialized...")

    # Representation of Product objects
    def __repr__(self) -> str:
        text = "[PRODUCT] List of Production Methods Begin\n-----------------------------------\n"
        methods = []
        # Read production methods from JSON file
        with open(self.product_data, "r") as file:
            try:
                methods = json.load(file)
            except json.decoder.JSONDecodeError:
                return "[PRODUCT] No production method exists\n"
        # Add each production method's information to the representation
        for method in methods:
            text += str(method) + "\n"
        text += "\n-----------------------------------\n[INVENTORY] List of Inventory End\n"
        return text

    # Method to add or update a production method
    def add_production_method(self, name, raw_materials, labor_hour):
        products = []
        # Read existing production methods from JSON file
        with open(self.product_data, "r+") as file:
            try:
                products = json.load(file)
            except json.decoder.JSONDecodeError:
                # If the file is empty, add the first production method
                json.dump(
                    [{"name": name, "raw_materials": raw_materials, "labor_hours": labor_hour}], file)
                print("[PRODUCT] Added new production method for {product}\n".format(
                    product=name))
                return

        # Check if the production method already exists
        for product in products:
            if product["name"] == name:
                product["raw_materials"] = raw_materials
                product["labor_hours"] = labor_hour
                message = "[PRODUCT] Updated production method for {product}\n".format(
                    product=name)
                break
        else:
            # If not, add the new production method
            products.append(
                {"name": name, "raw_materials": raw_materials, "labor_hours": labor_hour})
            message = "[PRODUCT] Added new production method for {product}\n".format(
                product=name)

        # Write the updated production methods to the JSON file
        with open(self.product_data, "w") as file:
            json.dump(products, file)
            print(message)
            return

    # Method to initiate production of a specific product
    def start_production(self, produce, quantity, employee, labor_budget):
        material_cost = 0
        labor_cost = 0
        total_cost = 0

        products = []
        # Read production methods from JSON file
        with open(self.product_data, "r+") as file:
            try:
                products = json.load(file)
            except json.decoder.JSONDecodeError:
                print("[PRODUCT] No production method exists\n")
                return

        # Check if the specified product exists in production methods
        for product in products:
            if product["name"] == produce:
                # Process raw materials required for production
                for item, amount in product["raw_materials"].items():
                    raw_material = inv.transfer_to_production(
                        item, produce, amount*quantity)
                    if raw_material[0] == True:
                        material_cost += raw_material[1]
                        total_cost += raw_material[1]
                    else:
                        print("[PRODUCT] Aborting production of {produce} due to insufficient inventory\n".format(
                            produce=produce))
                        return
                # Engage employee for labor
                labor = emp.engage_employee(
                    employee, produce, product["labor_hours"]*quantity, labor_budget)
                if labor[0] == True:
                    labor_cost += labor[1]
                    total_cost += labor[1]
                else:
                    print("[PRODUCT] Aborting production of {produce} due to insufficient labor budget\n".format(
                        produce=produce))
                    return

                # Calculate overhead cost
                overhead_cost = material_cost * 0.1 + labor_cost * 0.15
                total_cost += overhead_cost

                # Log the production details in the product log CSV file
                with open(self.product_log, "a") as file:
                    csv.DictWriter(file, fieldnames=product_log_headers, delimiter=';').writerow(
                        {"date": date.today(), "product": produce, "quantity": quantity, "material_cost": material_cost,
                         "labor_cost": labor_cost, "overhead_cost": overhead_cost, "total_cost": total_cost}
                    )
                print("[PRODUCT] Produced {unit} units of {product} @ Tk.{cost} total cost\n".format(
                    unit=quantity, product=produce, cost=total_cost))
                return
        else:
            print("[PRODUCT] No production method found for {produce}\n".format(
                produce=produce))
            return

    # Method to generate a production report
    def generate_report(self):
        # Copy the product log CSV file to create a production report
        system("cp .csv/product_log.csv \"Production Report\".csv")
