def blank_user(username, password, email):
    return {
        "username": username,
        "password": password,
        "email": email
    }

def blank_profile(user_id, email, **values):
    return {
        "user_id": user_id,
        "first_name": values["first_name"],
        "last_name": values["last_name"],
        "sex": values["sex"],
        "phone_number": values["phone_number"],
        "email": email,
        "dob": values["dob"],
        "role": values["role"],
        "link": values["link"]
    }