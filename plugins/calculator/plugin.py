import re

def calculate(expression):
    try:
        # Remove any non-numeric characters and evaluate the expression
        sanitized_expression = re.sub(r'[^\d+\-*/().]', '', expression)
        result = eval(sanitized_expression)

        return f"The result of the calculation is: {result}"
    except Exception as e:
        return f"Sorry, there was an error while performing the calculation: {str(e)}"
