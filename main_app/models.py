from bson.timestamp import Timestamp
from datetime import datetime

def blank_user(username, password, email, **kwargs):
    return {
        "username": username,
        "password": password,
        "email": email
    }

def blank_profile(user_id, email, **kwargs):
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
        "first_name": kwargs["first_name"],
        "last_name": kwargs["last_name"],
        "sex": kwargs["sex"],
        "phone_number": kwargs["phone_number"],
        "email": email,
        "dob": kwargs["dob"],
        "role": kwargs["role"],
        "link": kwargs["link"]
    }

def blank_post(user_id, title, body, votes=0, **kwargs):
    return {
        "user_id": user_id,
        "title": title,
        "body": body,
        "votes": votes,
        "timestamp": Timestamp(datetime.now(), 1)
    }

def blank_reply(user_id, post_id, body, votes=0, **kwargs):
    return {
        "user_id": user_id,
        "post_id": post_id,
        "body": body,
        "votes": votes,
        "timestamp": Timestamp(datetime.now(), 1)
    }