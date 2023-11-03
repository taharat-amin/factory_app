from datetime import date
from os import system
import json
import csv

employee_log_headers = ["date", "employee", "product", "hours", "cost"]


class Employee:
    employee_data = '.json/employees.json'
    employee_log = '.csv/employee_log.csv'
    # Initialize the Employee class

    def __init__(self, main_screen_init=False) -> None:
        if main_screen_init:
            print("[EMPLOYEE] Employees logged in...\n")

    # Representation of Employee objects
    def __repr__(self):
        # Initialize text with header
        text = ""
        employees = []
        # Read employee data from JSON file
        with open(self.employee_data, "r") as file:
            try:
                employees = json.load(file)
            except json.decoder.JSONDecodeError:
                return "[EMPLOYEE] No employee enlisted\n"

        longest_name = len("Name")
        longest_address = len("Address")
        longest_contact = len("Contact")
        longest_wage = len("Hourly Wage")

        for employee in employees:
            if len(employee["name"]) > longest_name:
                longest_name = len(employee["name"])
            if len(employee["address"]) > longest_address:
                longest_address = len(employee["address"])
            if len(employee["contact"]) > longest_contact:
                longest_contact = len(employee["contact"])
            if len(str(employee["hourly_wage"])) > longest_wage:
                longest_wage = len(str(employee["hourly_wage"]))

        text += "Employees".center(longest_name+longest_address +
                                   longest_contact+longest_wage+11)+"\n"
        text += "-"*(longest_name+longest_address +
                     longest_contact+longest_wage+11)+"\n"
        text += "Name"+" " * \
            (longest_name-len("Name"))+" | "
        text += "Address"+ \
            " "*(longest_address-len("Address"))+" | "
        text += "Contact"+ \
            " "*(longest_contact-len("Contact"))+" | "
        text += "Hourly Wage"+ \
            " "*(longest_wage-len("Hourly Wage"))+" |\n"
        text += "-"*(longest_name+1)+"+"+"-"*(longest_address+2) + \
            "+"+"-"*(longest_contact+2)+"+"+"-"*(longest_wage+3)+"\n"

        for employee in employees:

            text += "{name} | {address} | {contact} | {wage} |\n".format(
                name=employee["name"].ljust(longest_name),
                address=employee["address"].ljust(longest_address),
                contact=employee["contact"].ljust(longest_contact),
                wage=str(employee["hourly_wage"]).rjust(longest_wage)
            )
        text += "-"*(longest_name+longest_address +
                     longest_contact+longest_wage+11)+"\n"

        return text

    # Add a new employee to the system
    def add_employee(self, name, address, contact, hourly_wage):
        employees = []
        # Read existing employees from JSON file
        with open(self.employee_data, "r+") as file:
            try:
                employees = json.load(file)
            except json.decoder.JSONDecodeError:
                # If the file is empty, add the first employee
                json.dump([{"name": name, "address": address,
                          "contact": contact, "hourly_wage": hourly_wage}], file)
                print("\033[92m\n[EMPLOYEE] \033[0m", end='')
                print("Enlisted {name} as employee @ Tk.{wage}/hour rate\n".format(
                    name=name, wage=hourly_wage))
                return

        # Check if the employee already exists
        for employee in employees:
            if employee["name"] == name:
                print("\033[91m\n[EMPLOYEE] \033[0m", end='')
                print(
                    "Employee {name} already enlisted\n".format(name=name))
                return
        else:
            # If not, add the new employee
            employees.append({"name": name, "address": address,
                              "contact": contact, "hourly_wage": hourly_wage})

        # Write the updated employee data to the JSON file
        with open(self.employee_data, "w") as file:
            json.dump(employees, file)
        print("\033[92m\n[EMPLOYEE] \033[0m", end='')
        print("Enlisted {name} as employee @ Tk.{wage}/hour rate\n".format(
            name=name, wage=hourly_wage))

    # Engage an employee for a specific project
    def engage_employee(self, name, product, hours, budget):
        employees = []
        # Read employee data from JSON file
        with open(self.employee_data, "r") as file:
            employees = json.load(file)

        # Check if the employee exists
        for employee in employees:
            if employee["name"] == name:
                wage = employee["hourly_wage"] * hours
                # Check if the project budget is sufficient for the employee's wage
                if wage <= budget:
                    # If yes, log the employee's work in the CSV file
                    with open(self.employee_log, "a") as file:
                        csv.DictWriter(file, fieldnames=employee_log_headers, delimiter=';').writerow(
                            {"date": date.today(), "employee": name,
                             "product": product, "hours": hours, "cost": wage}
                        )
                    print("\033[92m\n[EMPLOYEE] \033[0m", end='')
                    print("Added labor worth {wage} from {employee}\n".format(
                        wage=wage, employee=name))
                    return True, wage
                else:
                    # If not, print a message indicating insufficient budget
                    print("\033[91m\n[EMPLOYEE] \033[0m", end='')
                    print("Wage of {employee} is Tk.{wage} higher than budget\n".format(
                        employee=name, wage=wage - budget))
                    return False, 0

    # Generate log report
    def generate_report(self):
        system("cp .csv/employee_log.csv \"Employee Log Report\".csv")
        print("\033[93m\n[EMPLOYEE] \033[0m", end='')
        print("Generated employee log report\n")
