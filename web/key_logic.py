import json
import uuid


def get_products() -> list:
    with open('static/items.json', 'r') as f:
        data = json.load(f)

    products = list(map(lambda product: product['name'], data))
    return products


def retrieve_keys() -> list:
    with open('keys.json', 'r') as f:
        data = json.load(f)

    keys = list(map(lambda product_keys: product_keys, data.values()))
    keys = [key for sublist in keys for key in sublist]

    return keys


def generate_key()-> str:
    key = str(uuid.uuid4())
    while key in retrieve_keys():
        key = str(uuid.uuid4())
    return key


def add_key(product: str) -> None:
    """
        Add a new key for a given product.
        
        Parameters:
        product (str): The product for which a new key should be added.
    """
    if product in get_products():
        with open('keys.json', 'r') as f:
            data = json.load(f)
        if product in json.load(open("keys.json", "r")).keys():
            data[product].append(generate_key())
        else:
            data[product] = [generate_key()]

        with open('keys.json', 'w') as f:
            json.dump(data, f)
        print(data)


def check_key(key: str, product: str) -> bool:
    """
        Check if a key is valid for a given product.

        Parameters:
        key (str): The key to be checked.
        product (str): The product for which the key is being checked.

        Returns:
        bool: True if the key is valid for the given product, False otherwise.
    """
    if key in retrieve_keys():
        print("key")
        if product in json.load(open("keys.json", "r")).keys():
            print("product")
            if key in json.load(open("keys.json", "r"))[product]:
                print("keyproduct")
                return True

    return False
    


