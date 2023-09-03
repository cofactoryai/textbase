from textbase import bot, Message
from typing import List

gadgets = {
    "1": {
        "name": "Smartphone X",
        "description": "A high-end smartphone with a powerful processor and stunning display.",
        "specifications": "Processor: Snapdragon 888\nRAM: 8GB\nStorage: 128GB\nCamera: 48MP",
        "price": "$299"
    },
    "2": {
        "name": "Laptop Y",
        "description": "A sleek and lightweight laptop with long battery life.",
        "specifications": "Processor: Intel Core i7\nRAM: 16GB\nStorage: 512GB SSD\nScreen: 13.3 inches",
        "price": "$1299"
    },
    "3": {
        "name": "Tablet Z",
        "description": "A versatile tablet with a high-resolution display.",
        "specifications": "Processor: MediaTek\nRAM: 4GB\nStorage: 64GB\nDisplay: 10.1 inches",
        "price": "$399"
    },
    "4": {
        "name": "Smartwatch A",
        "description": "A stylish smartwatch with health tracking features.",
        "specifications": "Screen Size: 1.3 inches\nBattery Life: Up to 7 days\nWater Resistance: Yes",
        "price": "$199"
    },
    "5": {
        "name": "Gaming Console B",
        "description": "A powerful gaming console for immersive gaming experiences.",
        "specifications": "GPU: AMD Radeon RDNA 2\nStorage: 1TB SSD\nGames: Supports 4K gaming",
        "price": "$999"
    },
    "6": {
        "name": "Bluetooth Speaker C",
        "description": "A portable Bluetooth speaker with high-quality sound.",
        "specifications": "Speaker Power: 20W\nBattery Life: Up to 10 hours\nConnectivity: Bluetooth 5.0",
        "price": "$79"
    },
    "7": {
        "name": "Headphones D",
        "description": "Over-ear headphones with noise-canceling technology.",
        "specifications": "Driver Size: 40mm\nNoise Cancellation: Yes\nBattery Life: Up to 20 hours",
        "price": "$149"
    },
    "8": {
        "name": "Digital Camera E",
        "description": "A professional-grade digital camera for photography enthusiasts.",
        "specifications": "Sensor Type: Full-frame\nMegapixels: 24MP\nLens: Interchangeable",
        "price": "$1999"
    },
    "9": {
        "name": "Fitness Tracker F",
        "description": "A fitness tracker with heart rate monitoring and sleep tracking.",
        "specifications": "Display: OLED\nHeart Rate Monitoring: Yes\nBattery Life: Up to 7 days",
        "price": "$69"
    },
    "10": {
        "name": "Smart Home Hub G",
        "description": "A central hub for controlling smart home devices.",
        "specifications": "Compatibility: Works with Alexa, Google Assistant\nConnectivity: Wi-Fi, Zigbee",
        "price": "$129"
    },
    "11": {
        "name": "E-book Reader H",
        "description": "An e-book reader with an E-Ink display for comfortable reading.",
        "specifications": "Screen Size: 6 inches\nStorage: 8GB\nBattery Life: Weeks",
        "price": "$99"
    },
    "12": {
        "name": "Drone I",
        "description": "A compact drone with 4K camera and GPS navigation.",
        "specifications": "Camera: 4K UHD\nFlight Time: Up to 30 minutes\nGPS: Yes",
        "price": "$599"
    },
    "13": {
        "name": "VR Headset J",
        "description": "A virtual reality headset for immersive gaming and experiences.",
        "specifications": "Display Type: OLED\nResolution: 2160x1200\nControllers: Included",
        "price": "$399"
    },
    "14": {
        "name": "Wireless Mouse K",
        "description": "A wireless mouse for precise and comfortable computing.",
        "specifications": "DPI: 1600\nConnectivity: USB receiver\nBattery Life: Up to 12 months",
        "price": "$29"
    },
    "15": {
        "name": "Portable Power Bank L",
        "description": "A high-capacity power bank for charging devices on the go.",
        "specifications": "Capacity: 20,000mAh\nOutput Ports: 2 USB\nFast Charging: Yes",
        "price": "$49"
    },
}

@bot()
def on_message(message_history: List[Message], state: dict = None):
    user_message = message_history[-1]["content"][0]["value"].lower()
    if "price of" in user_message:
        product_name = extract_product_name(user_message)
        if product_name:
            price = get_product_price(product_name)
            if price is not None:
                bot_response = f"The price of {product_name.capitalize()} is {price}."
            else:
                bot_response = f"Sorry, I couldn't find the price for {product_name.capitalize()}."
        else:
            bot_response = "I couldn't identify the product you're asking about."
    elif "specifications of" in user_message:
        product_name = extract_product_name(user_message)
        if product_name:
            specifications = get_product_specifications(product_name)
            if specifications is not None:
                bot_response = f"Here are the specifications of {product_name.capitalize()}:\n{specifications}"
            else:
                bot_response = f"Sorry, I couldn't find the specifications for {product_name.capitalize()}."
        else:
            bot_response = "I couldn't identify the product you're asking about."
    elif "specifications" in user_message:
        bot_response = "Sure, here are the specifications of some gadgets:\n"
        for product_id, product_data in gadgets.items():
            bot_response += f"{product_data['name']} - {product_data['specifications']}\n"
    elif "prices" in user_message:
        bot_response = "Here are the prices of some gadgets:\n"
        for product_id, product_data in gadgets.items():
            bot_response += f"{product_data['name']} - {product_data['price']}\n"
    elif "recommend" in user_message:
        recommended_products = recommend_products(gadgets, user_message)
        if recommended_products:
            bot_response = "Here are some recommended gadgets:\n"
            for product_data in recommended_products:
                bot_response += f"{product_data['name']} - {product_data['description']}\n"
        else:
            bot_response = "I'm sorry, I couldn't find any products that match your criteria."
    elif "thanks" in user_message or "thank you" in user_message:
        bot_response = "You're welcome! If you have any more questions, feel free to ask."
    else:
        bot_response = "Sure, I can help you with information about gadgets. You can ask about specifications, prices, or recommendations."

    response = {
        "data": {
            "messages": [
                {
                    "data_type": "STRING",
                    "value": bot_response
                }
            ],
            "state": state
        },
        "errors": []
    }

    return {
        "status_code": 200,
        "response": response
    }

def recommend_products(gadgets, user_message):
    recommended_products = []

    if "budget" in user_message:
        max_price = 500
        for product_id, product_data in gadgets.items():
            price = int(product_data['price'].replace('$', ''))
            if price <= max_price:
                recommended_products.append(product_data)
    elif "camera" in user_message:
        for product_id, product_data in gadgets.items():
            if "camera" in product_data['specifications'].lower():
                recommended_products.append(product_data)

    return recommended_products

def extract_product_name(user_message):
    parts = user_message.split("price of")
    if len(parts) > 1:
        return parts[1].strip()
    parts = user_message.split("specifications of")
    if len(parts) > 1:
        return parts[1].strip()
    return None

def get_product_price(product_name):
    for product_id, product_data in gadgets.items():
        if product_data['name'].lower() == product_name.lower():
            return product_data['price']
    return None

def get_product_specifications(product_name):
    for product_id, product_data in gadgets.items():
        if product_data['name'].lower() == product_name.lower():
            return product_data['specifications']
    return None
