import re


def validate_name(name):
    if not name or not name.strip():
        return False, "Name is required."

    name = name.strip()

    if len(name) < 2:
        return False, "Name must contain at least 2 characters."

    if not re.fullmatch(r"[A-Za-z ]+", name):
        return False, "Name can contain only letters and spaces."

    return True, ""


def validate_email(email):
    if not email or not email.strip():
        return False, "Email is required."

    email = email.strip()

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.fullmatch(pattern, email):
        return False, "Enter a valid email address."

    return True, ""


def validate_phone(phone):
    if not phone or not phone.strip():
        return False, "Phone number is required."

    phone = phone.strip()

    if not re.fullmatch(r"\d{10}", phone):
        return False, "Phone number must contain exactly 10 digits."

    return True, ""


def validate_record(name, email, phone):
    valid, message = validate_name(name)

    if not valid:
        return False, message

    valid, message = validate_email(email)

    if not valid:
        return False, message

    valid, message = validate_phone(phone)

    if not valid:
        return False, message

    return True, "Valid record."