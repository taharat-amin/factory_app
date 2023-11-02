product_log_headers = ["date", "product", "material_cost", "labor_cost", "overhead_cost", "total_cost"]

class Product:

    product_data = '.products.json'
    finished_goods_data = '.finished_goods.csv'

    def __init__(self) -> None:

        print("[PRODUCT] Product object initialized...")

    def __repr__(self) -> str:

        return "This class manages finished goods inventory of the factory"