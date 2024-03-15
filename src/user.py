#!/bin/python3

import data_store, re
from datetime import datetime

empty_list_length = 0

# Create new user with unique email, strong password and other details (note weight is in kg)
# Format: {userId: [{name: n}, {email: e}, {password: p}, {weight: w}, {target: 0}, {log: [{date: [f]}]}]}
def create_user(name, email, password, current_weight):
    data = data_store.get_data()
    app_users = data["users"]
    # Check email has not been taken
    if get_user_info(email) != None:
        raise ValueError("Email has already been taken. Try another one")
        
    # Check password is strong enough
    password_check = is_password_strong(password)
    if len(password_check) > empty_list_length:
        raise ValueError(password_check)
        
    # Creating new account
    new_ID = get_new_ID(app_users)
    today_date = datetime.today().date()
    new_user_info = {new_ID: [{"name": name}, {"email": email}, {"password": password}, {"weight": current_weight}, {"target": 0}, {"log": [{today_date: []}]}]}
    data_store.set_data(new_user_info)


# Helper function: Get user info
def get_user_info(email):
    data = data_store.get_data()
    app_users = data["users"]
    for user in app_users:
        user_email = user.values().get("email")
        if user_email == email:
            return user
    return None   

# Helper function: Checks if passwork is strong (uppercase + lowercase, numbers, special characters, at least 8 characters)
def is_password_strong(password):
    password_failures = []

    min_password_length = 8
    if len(password) < min_password_length:
        password_failures.append("Password needs to be at least 8 characters")

    if not re.search(password, "[a-z]+"):
        password_failures.append("Password needs at least one lowercase character")

    if not re.search(password, "[A-Z]+"):
        password_failures.append("Password needs at least one uppercase character")

    if not re.search(password, "\d+"):
        password_failures.append("Password needs at least one number")

    if not re.search(password, "[!@#$%^&*()\-_=+\[\]{};:'\",.<>?]+"):
        password_failures.append("Password needs at least one special character")

    return password_failures

# Helper function: From existing database creates new user ID, starts from 1 and increments by 5
def get_new_ID(user_info):
    return 5 * len(user_info) - 4

# Logs the user in with input username (email) and password or returns error if either are incorrect
def login(username, password):
    if is_nonexistent_username(username):
        raise ValueError("User not found")
    
    if is_wrong_password(username, password):
        raise ValueError("Wrong password")
    
    print("You are now logged in")
    return True

# Helper function: Goes through data.json to check if username exists
def is_nonexistent_username(username):
    if get_user_info(username) == None:
        return True
    return False

# Helper function: Checks that password for user account is correct
# Username already checked to exist so do not need to worry
def is_wrong_password(username, password):
    user = get_user_info(username)
    if password == user.values().get("password"):
        return False
    return True
