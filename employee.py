from datetime import date
import json
import csv

employee_log_headers = ["date", "employee", "product", "hours", "cost"]


class Employee:

    employee_data = ".json/employees.json"
    employee_log = ".csv/employee_log.csv"

    def __init__(self) -> None:

        print("[EMPLOYEE] Employee object initialized...\n")

    def __repr__(self):

        text = "[EMPLOYEE] List of Employees Begin\n-----------------------------------\n"
        employees = []
        with open(self.employee_data, "r") as file:
            try:
                employees = json.load(file)
            except json.decoder.JSONDecodeError:
                return "[EMPLOYEE] No employee enlisted\n"
        
        for employee in employees:
            text += str(employee)+"\n"
        text += "-----------------------------------\n[EMPLOYEE] List of Employees End\n"
        
        return text

    def add_employee(self, name, address, contact, hourly_wage):

        employees = []
        with open(self.employee_data, "r+") as file:
            try:
                employees = json.load(file)
            except json.decoder.JSONDecodeError:
                json.dump([{"name": name, "address": address,
                          "contact": contact, "hourly_wage": hourly_wage}], file)
                print("[EMPLOYEE] Enlisted {name} as employee @ Tk.{wage}/hour rate\n".format(
                    name=name, wage=hourly_wage))
                return

        for employee in employees:
            if employee["name"] == name:
                print(
                    "[EMPLOYEE] Employee {name} already enlisted\n".format(name=name))
                return
        else:
            employees.append({"name": name, "address": address,
                              "contact": contact, "hourly_wage": hourly_wage})

        with open(self.employee_data, "w") as file:
            json.dump(employees, file)
        print("[EMPLOYEE] Enlisted {name} as employee @ Tk.{wage}/hour rate\n".format(
            name=name, wage=hourly_wage))

    def engage_employee(self, name, product, hours, budget):

        employees = []
        with open(self.employee_data, "r") as file:
            employees = json.load(file)

        for employee in employees:
            if employee["name"] == name:
                wage = employee["hourly_wage"]*hours
                if wage <= budget:
                    with open(self.employee_log, "a") as file:
                        csv.DictWriter(file, fieldnames=employee_log_headers, delimiter=';').writerow(  # ["date", "employee", "product", "hours", "cost"]
                            {"date": date.today(), "employee": name,
                             "product": product, "hours": hours, "cost": wage}
                        )
                    print("[EMPLOYEE] Added labor worth {wage} from {employee}\n".format(
                        wage=wage, employee=name))
                    return True, wage
                else:
                    print("[EMPLOYEE] Wage of {employee} is Tk.{wage} higher than budget\n".format(employee=name, wage=wage-budget))
                    return False
