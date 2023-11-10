import re
import twilio 
from twilio.rest import Client

class Twilio:
    account_sid = None
    auth_token = None
    phonenumber = None
    msgServiceSid = None

    @classmethod
    def sendsms(
        cls,
        details: str,
        send_to: str,
    ):
        try:
            print("Sending Whatsapp message........")
            client = Client(cls.account_sid, cls.auth_token)
            message = client.messages.create(
                from_='whatsapp:'+cls.phonenumber,
                messaging_service_sid=cls.msgServiceSid,
                body=details,
                to='whatsapp:+91'+send_to
            )
            print("Message Sent to Whatsapp Successfully")
        except Exception as e:
            print("Whatsapp message not sent due to :",e)

    @classmethod
    def extract_phone_number(cls, input_string:str):
        # Define a regular expression pattern to match 10-digit phone numbers
        # Create this according to you country code
        phone_number_pattern = r'\b\d{10}\b'

        # Find all phone numbers in the input string
        phone_numbers = re.findall(phone_number_pattern, input_string)

        if phone_numbers:
            # Phone number(s) found, return the first one
            print("User phone number found : ", phone_numbers[0] ) 
            return phone_numbers[0]
        else:
            # No phone numbers found
            return None    