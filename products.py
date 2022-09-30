from dataclasses import dataclass

@dataclass 
class Product:
    """
        Class that represents an entity in the database
    """
    name: str
    unit_price: float 
    quantity: int
 

class ListOfProducts:
    _products = []

    def __init__(self, *args):
        self._products += list(args)
    
    def add(self, product: dict):
        self._products.append(
            Product(
                name=product['name'],
                unit_price=product['price'],
                quantity=product['quantity']
            )
        )

    def remove(self, product: Product):
        self._products.remove(product)

    def pop(self):
        value = self._products.pop()
        return value

    def __len__(self):
        return len(self._products)
