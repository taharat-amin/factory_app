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
        print("[PRODUCT] Production started...\n")

    # Representation of Product objects
    def __repr__(self) -> str:
        text = ""
        methods = []
        # Read production methods from JSON file
        with open(self.product_data, "r") as file:
            try:
                methods = json.load(file)
            except json.decoder.JSONDecodeError:
                print("\033[91m\n[PRODUCT]  \033[0m", end='')
                return "No production method exists\n"

        longest_name = len("Name")
        longest_rm = len("Required DM")
        longest_labor = len("Required DL")
        for method in methods:
            if len(method["name"]) > longest_name:
                longest_name = len(method["name"])
            if len(str(method["raw_materials"])) > longest_rm:
                longest_rm = len(str(method["raw_materials"]))
            if len(str(method["labor_hours"])) > longest_labor:
                longest_labor = len(str(method["labor_hours"]))

        text += "Production Methods".center(longest_name +
                                            longest_labor+longest_rm+8)+"\n"
        text += "-"*(longest_name+longest_labor+longest_rm+8)+"\n"
        text += "Name"+" "*(longest_name-len("Name"))+" | "
        text += "Required DM"+" "*(longest_rm-len("Required DM"))+" | "
        text += "Required DL"+" "*(longest_labor-len("Required DL"))+" |\n"
        text += "-"*(longest_name+1)+"+"+"-" * \
            (longest_rm+2)+"+"+"-"*(longest_labor+3)

        for method in methods:
            text += "{name} | {rm} | {dl} |\n".format(
                name=method["name"].ljust(longest_name),
                rm=str(method["raw_materials"]).ljust(longest_rm),
                dl=str(method["labor_hours"]).rjust(longest_labor)
            )

        text += "-"*(longest_name+longest_labor+longest_rm+8)+"\n"

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
                print("\033[93m\n[PRODUCT] \033[0m", end='')
                print("Added new production method for {product}\n".format(
                    product=name))
                return

        # Check if the production method already exists
        for product in products:
            if product["name"] == name:
                product["raw_materials"] = raw_materials
                product["labor_hours"] = labor_hour
                print("\033[93m\n[PRODUCT] \033[0m", end='')
                message = "Updated production method for {product}\n".format(
                    product=name)
                break
        else:
            # If not, add the new production method
            products.append(
                {"name": name, "raw_materials": raw_materials, "labor_hours": labor_hour})
            print("\033[93m\n[PRODUCT] \033[0m", end='')
            message = "Added new production method for {product}\n".format(
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
                print("\033[91m\n[PRODUCT] \033[0m", end='')
                print("No production method exists\n")
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
                        print("\033[91m\n[PRODUCT] \033[0m", end='')
                        print("Aborting production of {produce} due to unavilability of raw material\n".format(
                            produce=produce))
                        return
                # Engage employee for labor
                labor = emp.engage_employee(
                    employee, produce, product["labor_hours"]*quantity, labor_budget)
                if labor[0] == True:
                    labor_cost += labor[1]
                    total_cost += labor[1]
                else:
                    if labor[1] == 0:
                        print("\033[91m\n[PRODUCT] \033[0m", end='')
                        print("Aborting production of {produce} due to insufficient labor budget\n".format(
                            produce=produce))
                        return
                    else:
                        print("\033[91m\n[PRODUCT] \033[0m", end='')
                        print("Aborting production of {produce} due to unavilability of labor\n".format(
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
                print("\033[92m\n[PRODUCT] \033[0m", end='')
                print("Produced {unit} units of {product} @ Tk.{cost} total cost\n".format(
                    unit=quantity, product=produce, cost=total_cost))
                return
        else:
            print("\033[91m\n[PRODUCT] \033[0m", end='')
            print("No production method found for {produce}\n".format(
                produce=produce))
            return

    # Method to generate a production report
    def generate_report(self):
        # Copy the product log CSV file to create a production report
        system("cp .csv/product_log.csv \"Production Report\".csv")
        print("\033[93m\n[PRODUCT] \033[0m", end='')
        print("Generated product cost report\n")
