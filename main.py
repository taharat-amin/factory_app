from inventory import Inventory
from employee import Employee

from os.path import exists
from os import system
import csv


# Placed in global scope because of use in multiple place of the code
product_headers = ["date", "product", "employee", "material_cost", "labor_cost", "total_cost"]
inventory_log_headers = ["date", "item", "product", "qty", "cost"]
employee_log_headers = ["date", "employee", "product", "hours", "cost"]

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

if not exists(".csv/employee_log.json"):
    system("touch .csv/employee_log.csv")
    with open(".csv/employee_log.csv", "w") as file:
        csv.DictWriter(file, fieldnames=employee_log_headers,
                       delimiter=';').writeheader()

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
inv.transfer_to_production("Copper", "Cables", 30)
