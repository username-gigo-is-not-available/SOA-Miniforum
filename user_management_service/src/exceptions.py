def user_not_found_message(user_id: int = None, email: str = None):
    if user_id:
        return f"User with user_id {user_id} was not found!"
    elif email:
        return f"User with email {email} was not found!"


def invalid_credentials_message():
    return "Invalid password!"


def email_already_taken_message(email: str):
    return f"Email {email} is already taken!"
