from inventory import Inventory, inventory_log_headers
from employee import Employee, employee_log_headers
from product import Product, product_log_headers

from os.path import exists
from os import system
from datetime import datetime
from datetime import timedelta
from time import sleep
import csv
import json
import sys
from hashlib import sha256
from getpass import getpass

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

if not exists(".csv/product_log.csv"):
    system("touch .csv/product_log.csv")
    with open(".csv/product_log.csv", "w") as file:
        csv.DictWriter(file, fieldnames=product_log_headers,
                       delimiter=';').writeheader()

if not exists(".fallback.txt"):
    system("touch .fallback.txt")

# Instantiate the objects
print("\n[SYSTEM] Initializing system...\n")
print("[DATA] Data storage initialized...\n")
inv = Inventory(main_screen_init=True)
emp = Employee(True)
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
print("\nWELCOME TO THE FACTORY MANAGEMENT SYSTEM\n")

# User creation segment
if not exists(".credentials.json"):
    system("touch .credentials.json")
    print("[SYSTEM] No user exists. Create a profile to continue\n")
    username = input("Enter username: ")
    while True:
        pass1 = getpass("Enter password: ")
        pass2 = getpass("Enter password again: ")
        if pass1 == pass2:
            with open(".credentials.json", "w") as file:
                json.dump({"username": username, "password": sha256(
                    pass1.encode('utf-8')).hexdigest()}, file)
            print("[SYSTEM] Profile creation successful\n")
            break
        else:
            print("[SYSTEM] Passwords do not match. Try again\n")
            continue


while True:
    # Check if the application is quarantined
    with open(".fallback.txt", "r") as fallback_file:
        quarantine = fallback_file.readlines()
        if len(quarantine) == 0:
            pass
        else:
            qtime = quarantine[0].strip()
            qtime = datetime.strptime(qtime, "%Y-%m-%d %H:%M:%S.%f")
            time_difference = datetime.now() - qtime
            time_delta = timedelta(hours=3)
            if time_difference >= time_delta:
                pass
            else:
                time = str(time_delta-time_difference)
                hours, minutes = time.split(':')[0:2]
                print("[SYSTEM] Application quarantined due to earlier suspicious activites. Try again after {hour} hours and {minute} minutes.\n".format(hour=hours, minute=minutes))
            sys.exit()
            
    # User login
    print("[SYSTEM] Please login to continue\n")
    logged_in = False
    wrong_pass_count = 4
    username = input("Enter username: ")

    with open(".credentials.json", "r") as file:
        creds = json.load(file)
        if creds["username"] != username:
            print("[SYSTEM] Username not found\n")
            continue

    while wrong_pass_count > 0:
        password = getpass("Enter password: ")
        if creds["password"] != sha256(password.encode('utf-8')).hexdigest():
            wrong_pass_count -= 1
            if wrong_pass_count == 0:
                print(
                    "\n[SYSTEM] Suspicious activity detected. Initiating fallback sequence...\n")
                sleep(3)
                with open(".fallback.txt", "w") as fallback_file:
                    fallback_file.writelines(str(datetime.now()))
                print("[SYSTEM] System locked down for 3 hours due to suspicious activity.\n")
                sys.exit()
            print("\n[SYSTEM] Wrong password. {count} attempts left.\n".format(
                count=wrong_pass_count))
        else:
            logged_in = True
            break

    if logged_in:
        # Perform actions after successful login
        print("\n[SYSTEM] Login successful. Welcome {username}\n".format(username=username))
        # Add your code for actions to be performed after successful login here
        pass
