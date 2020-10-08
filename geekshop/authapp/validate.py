import re


def password_validator(value):
    if not re.findall(r'\d', value) and not re.findall(r'[!?$*%^&#@]+', value):
        return True
    else:
        return False
