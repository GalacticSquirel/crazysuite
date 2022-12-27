# Install Courier SDK: pip install trycourier
from trycourier import Courier
import json
client = Courier(auth_token=json.load(open("secrets.json", "r"))["courierapi"])

def send(link: str, email: str):
    resp = client.send_message(
    message={
        "to": {
        "email": email
        },
        "content": {
        "title": "Verify Your Email",
        "body": "Click here to verify {{link}}"
        },
        "data": {"link":link}
    }
    )
    return resp