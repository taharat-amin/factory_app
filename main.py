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

if not exists(".csv/employee_log.csv"):
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

if not exists("./Reports"):
    system("mkdir Reports")

# Instantiate the objects
print("\n[SYSTEM] Initializing system...\n")
print("[DATA] Data storage initialized...\n")
inv = Inventory(main_screen_init=True)
emp = Employee(True)
pro = Product()
print("[SYSTEM] System initialized...")

print("""\n
█▀▀ ▄▀█ █▀▀ ▀█▀ █▀█ █▀█ █▄█   █▀▄▀█ ▄▀█ █▄░█ ▄▀█ █▀▀ █▀▀ █▀▄▀█ █▀▀ █▄░█ ▀█▀   █▀ █▄█ █▀ ▀█▀ █▀▀ █▀▄▀█
█▀░ █▀█ █▄▄ ░█░ █▄█ █▀▄ ░█░   █░▀░█ █▀█ █░▀█ █▀█ █▄█ ██▄ █░▀░█ ██▄ █░▀█ ░█░   ▄█ ░█░ ▄█ ░█░ ██▄ █░▀░█\n""")
print("\n-----------------------\n|Developer Information|\n|TAHARAT AMIN         |\n|DHAKA, BANGLADESH    |\n|GITHUB: taharat-amin |\n-----------------------\n\n")

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
                json.dump([{"username": username, "password": sha256(
                    pass1.encode('utf-8')).hexdigest()}], file)
            print("\n[SYSTEM] Profile creation successful\n")
            break
        else:
            print("\n[SYSTEM] Passwords do not match. Try again\n")
            continue


def add_user(username, password):
    users = []
    with open(".credentials.json", "r") as file:
        users = json.load(file)

    users.append({"username": username, "password": sha256(
        password.encode('utf-8')).hexdigest()})
    with open(".credentials.json", "w") as file:
        json.dump(users, file)

    print("\n[SYSTEM] Added new user\n")


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
                print("[SYSTEM] Application quarantined due to earlier suspicious activites. Try again after {hour} hours and {minute} minutes.\n".format(
                    hour=hours, minute=minutes))
            sys.exit()

    # User login
    print("[SYSTEM] Please login to continue\n(Press 'ctrl+c' to exit application)\n")
    logged_in = False
    wrong_pass_count = 4

    try:
        username = input("Enter username: ")
    except KeyboardInterrupt:
        print("\n[SYSTEM] Exiting application")
        sys.exit()

    user_pass = ''
    user_found = False

    with open(".credentials.json", "r") as file:
        creds = json.load(file)
        for cred in creds:
            if cred["username"] == username:
                user_pass = cred["password"]
                user_found = True

    if user_found == False:
        print("[SYSTEM] Username not found\n")
        continue

    while wrong_pass_count > 0:

        try:
            password = getpass("Enter password: ")
        except KeyboardInterrupt:
            print("\n[SYSTEM] Exiting application")
            sys.exit()

        if user_pass != sha256(password.encode('utf-8')).hexdigest():
            wrong_pass_count -= 1
            if wrong_pass_count == 0:
                print(
                    "\n[SYSTEM] Suspicious activity detected. Initiating fallback sequence...\n")
                sleep(3)
                with open(".fallback.txt", "w") as fallback_file:
                    fallback_file.writelines(str(datetime.now()))
                print(
                    "[SYSTEM] System locked down for 3 hours due to suspicious activity.\n")
                sys.exit()
            print("\n[SYSTEM] Wrong password. {count} attempts left.\n".format(
                count=wrong_pass_count))
        else:
            logged_in = True
            break

    if logged_in:
        # Perform actions after successful login
        print("\n[SYSTEM] Login successful. Welcome {username}\n".format(
            username=username))
        # Actions to be performed after successful login here
        while True:
            # Ask user for management activity
            q1 = input(
                "[SYSTEM] What do you want to manage?\n(1) Inventory\n(2) Employees\n(3) Production\n(n) Create new user\n(q) Logout\nEnter option:\n")
            if q1 == "1":
                while True:
                    q2 = input(
                        "What activity do you want to perform?\n(1) View Inventory\n(2) Add items to inventory\n(3) Generate inventory log report\n(b) Go back to previous menu\n(n) Create new user\nEnter option:\n")
                    if q2 == "1":
                        print(inv)
                    elif q2 == "2":
                        inv.add_item(input("Enter the name of the inventory item: "), float(input(
                            "Enter the quantity of the item (numbers only): ")), float(input("Enter the purchase price per unit of the product: ")))
                    elif q2 == "3":
                        inv.generate_report()
                    elif q2 == "b":
                        break
                    else:
                        print("[SYSTEM] Option not recognized. Try again\n")
                        continue
            elif q1 == "2":
                while True:
                    q2 = input(
                        "What activity do you want to perform?\n(1) View Employees\n(2) Add new employee\n(3) Generate employee log report\n(b) Go back to previous menu\nEnter option:\n")
                    if q2 == "1":
                        print(emp)
                    elif q2 == "2":
                        emp.add_employee(input("Enter the name of the employee: "), input("Enter the address of the employee: "), input(
                            "Enter the contact number of the employee: "), float(input("Enter the hourly wage rate of the employee (numbers only): ")))
                    elif q2 == "3":
                        emp.generate_report()
                    elif q2 == "b":
                        break
                    else:
                        print("[SYSTEM] Option not recognized. Try again\n")
                        continue
            elif q1 == "3":
                while True:
                    q2 = input(
                        "What activity do you want to perform?\n(1) View production methods\n(2) Add or update production method\n(3) Start production\n(4) Generate production cost report\n(b) Go back to previous menu\nEnter option:\n")
                    if q2 == "1":
                        print(pro)
                    elif q2 == "2":
                        counter = int(input(
                            "How many raw materials are required to produce the product? (numbers only): "))
                        items = {}
                        while counter > 0:
                            item = input("Name of raw material: ")
                            items[item] = float(
                                input("Required quantity of raw material: "))
                            counter -= 1
                        pro.add_production_method(input("Enter name of the product: "), items, float(
                            input("Enter required labour hours: ")))
                    elif q2 == "3":
                        pro.start_production(input("Enter produce name: "), float(input("Enter the quantity to be produced: ")), input(
                            "Enter who will produce: "), float(input("Enter the budget for labor: ")))
                    elif q2 == "4":
                        pro.generate_report()
                    elif q2 == "b":
                        break
                    else:
                        print("[SYSTEM] Option not recognized. Try again\n")
                        continue
            elif q1 == "q":
                break
            elif q1 == "n":
                name = input("Enter username: ")
                p1 = getpass("Enter password: ")
                p2 = getpass("Enter password again: ")
                if p1 == p2:
                    add_user(name, p1)
            else:
                print("[SYSTEM] Option not recognized. Try again\n")
                continue
