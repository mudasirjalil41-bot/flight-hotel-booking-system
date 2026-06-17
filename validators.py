import re
def safe_str(msg):
    return input(msg).strip()

def safe_int(msg):
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("please enter a number.")


def safe_gmail(msg):
    """
    valid format
    letters+number+@gmail.com
    example ali123@gmail.com
    """
    pattern = r'^[a-zA-Z]+[0-9]+@gmail\.com$'

    while True:
        email = input(msg).strip()
        if re.match(pattern,email):
            return email
        else:
            print("invalid email")



