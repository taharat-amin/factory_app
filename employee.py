class Employee:

    employee_data = '.employees.json'

    def __init__(self) -> None:

        print("[EMPLOYEE] Employee object initialized...")

    def __repr__(self):

        return "This class manages employees of the factory"