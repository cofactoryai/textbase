import datetime

def get_current_time():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    return f"The current time is {current_time}."

def get_current_date():
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    return f"Today's date is {current_date}."
