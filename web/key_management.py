import json
import uuid
from typing import Union

key_to_product = {key: product for product, product_keys in json.load(open("keys.json", "r")).items() for key_dict in product_keys for key in key_dict}

def save(data):
    with open('keys.json', 'w') as f:
        json.dump(data, f, indent=4)


def get_products() -> list:
    with open('static/items.json', 'r') as f:
        data = json.load(f)

    products = list(map(lambda product: product['name'], data))
    return products

def get_product_url(product) -> Union[str, None]:
    with open('static/items.json', 'r') as f:
        items = json.load(f)

    return next((item["download_url"] for item in items if item["name"] == product), None)

def get_keys() -> list:
    with open('keys.json', 'r') as f:
        data = json.load(f)

    keys = list(map(lambda product_keys: product_keys, data.values()))
    keys = [key for sublist in keys for key in sublist]

    return keys


def get_keys_list() -> list:
    with open('keys.json', 'r') as f:
        data = json.load(f)
    keys = list(map(lambda product_keys: product_keys, data.values()))
    keys = [key for sublist in keys for key in sublist]
    keys = list(map(lambda x: list(x.keys())[0], keys))
    return keys


def get_keys_for_product(product: str) -> list:
    with open('keys.json', 'r') as f:
        keys = json.load(f)[product]
    keys = list(map(lambda x: list(x.keys())[0], keys))
    return keys


def generate_key() -> str:
    key = str(uuid.uuid4())
    while key in get_keys_list():
        key = str(uuid.uuid4())
    return key


def add_key(product: str) -> Union[str, bool]:
    """
        Add a new key for a given product.

        Parameters:
        product (str): The product for which a new key should be added.
        
        Returns:
            Union[str, bool]: If the key is successfully generated, returns the key. If the key is not, returns False.
    """
    if product in get_products():
        new_key = generate_key()
        with open('keys.json', 'r') as f:
            data = json.load(f)
        if product in json.load(open("keys.json", "r")).keys():
            data[product].append({new_key: None})
        else:
            data[product] = [{new_key: None}]

        save(data)
        print(data)
    else:
        return False
    return new_key


def check_key(key: str, product: str) -> bool:
    """
        Check if a key is valid for a given product.

        Parameters:
        key (str): The key to be checked.
        product (str): The product for which the key is being checked.

        Returns:
        bool: True if the key is valid for the given product, False otherwise.
    """
    if key in get_keys_list():
        if product in get_products():
            if key in get_keys_for_product(product):
                return True
    return False


def redeem(key: str, uid: int) -> Union[bool, str]:
    """
        Redeem a product key for the given user ID.
        
        Parameters:
            key (str): The product key to redeem.
            uid (int): The user ID to associate with the redeemed key.
            
        Returns:
            Union[bool, str]: If the key is successfully redeemed, returns the name of the product associated with the key. If the key is invalid, returns False.
    """
    with open("keys.json", "r") as f:
        data = json.load(f)


    product = key_to_product.get(key)

    if product is None:
        return False
    with open('keys.json', 'r') as f:
        keys = json.load(f)

    list(map(lambda product_key: product_key.update({key: uid}) if key in product_key else product_key, [
         product_key for product, product_keys in keys.items() for product_key in product_keys]))
    save(keys)
    return product


def owned_items(uid: int) -> dict:
    products = []
    for key in get_keys():
        if uid in key.values():
            products.append(key_to_product.get(list(key.keys())[0]))
    urls = list(map(lambda x: get_product_url(x), products))
    owned = dict(zip(products, urls))
    return owned
