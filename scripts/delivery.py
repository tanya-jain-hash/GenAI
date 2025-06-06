import requests
import random
import string
from utility import convert_text_to_speech, insert_to_db

def calculate_price(origin, destination):
    result = requests.get(f"https://api.distancematrix.ai/maps/api/distancematrix/json?origins={origin}&destinations={destination}&key=pm356qy72crK84bNZKgne3kpTXWbDx1QWTpr51FMh8NkqHN2KOwNlpUB25i11zF2")
    distance = float(result.json()["rows"][0]["elements"][0]["distance"]["text"].replace(" km",""))
    amount = round(4.8*1 + 100* (distance-1),2)
    return amount

def get_order_id(length = 8):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

def get_details():
    # flag=False
    # while flag:
    name = input("Please enter your name: ")
    mobile_no = int(input("Please enter your mobile no: "))
    origin = input("Please enter your address: ")
    destination = input("Please enter your destination address: ")
    confirmation_text = f"""Please confirm your details: 
                        Name {name}, 
                        mobile number {mobile_no},
                        your address {origin},
                        destination {destination}... 
                        Is this right?"""
    convert_text_to_speech(confirmation_text, "confimation_speech")
        # answer = input("confirm: ")
        # if answer=="yes":
        #     flag = True
        # else:
        #     flag=False    
    
    amount = calculate_price(origin, destination)
    convert_text_to_speech(f"You need to pay dollars {amount}. Please choose a payment mode: Cash or Card", "option_speech")
    option = input("Enter your choice")
    if option=="1":
        payment_mode = "Cash"
    else:
        payment_mode = "Card"
    order_id = get_order_id()

    insert_to_db(f"""Add row to shipment table with customer name as {name}
                customer mobile no as {mobile_no} 
                shipment_origin as {origin} 
                shipment_destination as {destination} 
                shipment_amount as {amount} , 
                payment_status as paid,
                payment_mode as {payment_mode}
                order_id as {order_id}""")
    return order_id

def main():
    order_id = get_details()
    return order_id

