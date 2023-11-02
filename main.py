class Inventory:
    
    def __init__(self):
        
        print("[MESSAGE] Inventory object inititated...")

    def __repr__(self):
        
        return "This class manages raw material inventory of the factory"


class Employee:
    
    def __init__(self) -> None:
        
        print("[MESSAGE] Employee object initiated...")

    def __repr__(self):
        
        return "This class manages employees of the factory"

class Product:
    
    def __init__(self) -> None:

        print("[MESSAGE] Product object initiated...")

    def __repr__(self) -> str:
        
        return "This class manages finished goods inventory of the factory"


inv = Inventory()
emp = Employee()
pro = Product()

print(inv)
print(emp)
print(pro)