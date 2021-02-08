from bson.timestamp import Timestamp
from datetime import datetime

def blank_user(username, password, email):
    return {
        "username": username,
        "password": password,
        "email": email
    }

def blank_profile(user_id, email, **values):
    if not values:
        return {
            "user_id": user_id,
            "first_name": None,
            "last_name": None,
            "sex": None,
            "phone_number": None,
            "email": email,
            "dob": None,
            "role": None,
            "link": None
        }
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

def blank_post(user_id, title, body, votes=0):
    return {
        "user_id": user_id,
        "title": title,
        "body": body,
        "votes": votes,
        "timestamp": Timestamp(datetime.now(), 1)
    }

def blank_reply(user_id, post_id, body, votes=0):
    return {
        "user_id": user_id,
        "post_id": post_id,
        "body": body,
        "votes": votes,
        "timestamp": Timestamp(datetime.now(), 1)
    }