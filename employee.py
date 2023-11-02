from datetime import date
from os import system
import json
import csv

employee_log_headers = ["date", "employee", "product", "hours", "cost"]

class Employee:
    employee_data = '.json/employees.json'
    employee_log = '.csv/employee_log.csv'
    # Initialize the Employee class
    def __init__(self) -> None:
        print("[EMPLOYEE] Employee object initialized...\n")

    # Representation of Employee objects
    def __repr__(self):
        # Initialize text with header
        text = "[EMPLOYEE] List of Employees Begin\n-----------------------------------\n"
        employees = []
        # Read employee data from JSON file
        with open(self.employee_data, "r") as file:
            try:
                employees = json.load(file)
            except json.decoder.JSONDecodeError:
                return "[EMPLOYEE] No employee enlisted\n"
        
        # Add each employee's information to the representation
        for employee in employees:
            text += str(employee)+"\n"
        text += "-----------------------------------\n[EMPLOYEE] List of Employees End\n"
        
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
                print("[EMPLOYEE] Enlisted {name} as employee @ Tk.{wage}/hour rate\n".format(
                    name=name, wage=hourly_wage))
                return

        # Check if the employee already exists
        for employee in employees:
            if employee["name"] == name:
                print("[EMPLOYEE] Employee {name} already enlisted\n".format(name=name))
                return
        else:
            # If not, add the new employee
            employees.append({"name": name, "address": address,
                              "contact": contact, "hourly_wage": hourly_wage})

        # Write the updated employee data to the JSON file
        with open(self.employee_data, "w") as file:
            json.dump(employees, file)
        print("[EMPLOYEE] Enlisted {name} as employee @ Tk.{wage}/hour rate\n".format(
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
                    print("[EMPLOYEE] Added labor worth {wage} from {employee}\n".format(
                        wage=wage, employee=name))
                    return True, wage
                else:
                    # If not, print a message indicating insufficient budget
                    print("[EMPLOYEE] Wage of {employee} is Tk.{wage} higher than budget\n".format(
                        employee=name, wage=wage - budget))
                    return False
                
    def generate_report(self):
        system("cp .csv/employee_log.csv \"Employee Log Report\".csv")