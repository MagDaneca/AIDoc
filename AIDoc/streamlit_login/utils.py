import re
import json
import courier
from courier.client import Courier
import secrets
from argon2 import PasswordHasher
import requests
from datetime import datetime, timedelta

ph = PasswordHasher() 

def check_usr_pass(username: str, password: str) -> bool:
    """
    Authenticates the username and password.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_user_data = json.load(auth_json)

    for registered_user in authorized_user_data:
        if registered_user['username'] == username:
            try:
                passwd_verification_bool = ph.verify(registered_user['password'], password)
                if passwd_verification_bool == True:
                    return True
            except:
                pass
    return False


def load_lottieurl(url: str) -> str:
    """
    Fetches the lottie animation using the URL.
    """
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        pass


def check_valid_name(name_sign_up: str) -> bool:
    """
    Checks if the user entered a valid name while creating the account.
    """
    name_regex = (r'^[A-Za-z_][A-Za-z0-9_]*')

    if re.search(name_regex, name_sign_up):
        return True
    return False


def check_valid_email(email_sign_up: str) -> bool:
    """
    Checks if the user entered a valid email while creating the account.
    """
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if re.fullmatch(regex, email_sign_up):
        return True
    return False


def check_unique_email(email_sign_up: str) -> bool:
    """
    Checks if the email already exists (since email needs to be unique).
    """
    authorized_user_data_master = list()
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user['email'])

    if email_sign_up in authorized_user_data_master:
        return False
    return True


def non_empty_str_check(username_sign_up: str) -> bool:
    """
    Checks for non-empty strings.
    """
    empty_count = 0
    for i in username_sign_up:
        if i == ' ':
            empty_count = empty_count + 1
            if empty_count == len(username_sign_up):
                return False

    if not username_sign_up:
        return False
    return True


def check_unique_usr(username_sign_up: str):
    """
    Checks if the username already exists (since username needs to be unique),
    also checks for non - empty username.
    """
    authorized_user_data_master = list()
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user['username'])

    if username_sign_up in authorized_user_data_master:
        return False
    
    non_empty_check = non_empty_str_check(username_sign_up)

    if non_empty_check == False:
        return None
    return True


def register_new_usr(name_sign_up: str, email_sign_up: str, username_sign_up: str, password_sign_up: str) -> None:
    """
    Saves the information of the new user in the _secret_auth.json file.
    """
    new_usr_data = {'username': username_sign_up, 'name': name_sign_up, 'email': email_sign_up, 'password': ph.hash(password_sign_up)}

    with open("_secret_auth_.json", "r") as auth_json:
        authorized_user_data = json.load(auth_json)

    with open("_secret_auth_.json", "w") as auth_json_write:
        authorized_user_data.append(new_usr_data)
        json.dump(authorized_user_data, auth_json_write)


def check_username_exists(user_name: str) -> bool:
    """
    Checks if the username exists in the _secret_auth.json file.
    """
    authorized_user_data_master = list()
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            authorized_user_data_master.append(user['username'])
        
    if user_name in authorized_user_data_master:
        return True
    return False
        

def check_email_exists(email_forgot_passwd: str):
    """
    Checks if the email entered is present in the _secret_auth.json file.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            if user['email'] == email_forgot_passwd:
                    return True, user['username']
    return False, None


def generate_random_passwd() -> str:
    """
    Generates a random password to be sent in email.
    """
    password_length = 10
    return secrets.token_urlsafe(password_length)


def send_passwd_in_email(auth_token: str, email_forgot_passwd: str, username_forgot_passwd: str, random_password: str):
    client = Courier(authorization_token="pk_prod_TSABQG9T12M5J7P5Q9ZCMN4XPT5N")
    
    # Generate expiration time (e.g., 24 hours from now)
    expiration_time = datetime.now() + timedelta(hours=24)
    expiration_iso = expiration_time.isoformat()

    resp = client.send(
        message=courier.ContentMessage(
            to=courier.UserRecipient(
                email=email_forgot_passwd
            ),
            content={
                'title': 'Забравена парола',
                'body': f'Потребителско име: {username_forgot_passwd}\nВременна парола: {random_password}\nПаролата изтича на: {expiration_iso}'
            },
            # If the API expects a top-level 'expiration' field
            expiration=expiration_iso
        )
    )
    return resp

def send_doc_email(auth_token: str, email_doc: str, user_name: str,specialty: str,city: str,username: str) -> None:
    """
    Triggers an email to the user containing the randomly generated password.
    """
    client = Courier(authorization_token = "pk_prod_TSABQG9T12M5J7P5Q91W4CK2HN75")

    resp = client.send_message(
    message={
        "to": {
        "email": email_doc
        },
        "content": {
        "title":"Здравейте," + user_name,
        "body": f"Здравейте {user_name}, този имейл е във връзка създаването на вашият акаунт в системата AIDoc, очаквайте съвсем скоро да се свърже нашият екип с вас!\n Данните които ни предоставихте: име: {user_name},потребителско име: {username}, специалности: {specialty}, град: {city}, имейл за връзка: {email_doc}"
        },
    }
    )


def change_passwd(email_: str, random_password: str) -> None:
    """
    Replaces the old password with the newly generated password.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

    with open("_secret_auth_.json", "w") as auth_json_:
        for user in authorized_users_data:
            if user['email'] == email_:
                user['password'] = ph.hash(random_password)
        json.dump(authorized_users_data, auth_json_)
    

def check_current_passwd(email_reset_passwd: str, current_passwd: str) -> bool:
    """
    Authenticates the password entered against the username when 
    resetting the password.
    """
    with open("_secret_auth_.json", "r") as auth_json:
        authorized_users_data = json.load(auth_json)

        for user in authorized_users_data:
            if user['email'] == email_reset_passwd:
                try:
                    if ph.verify(user['password'], current_passwd) == True:
                        return True
                except:
                    pass
    return False

def check_strong_password(password: str) -> bool:
    """
    Checks if the provided string is a strong password.
    """
    password_regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z\d\s]).{6,}$'

    if re.search(password_regex, password):
        return True
    return False

# Author: Gauri Prabhakar
# GitHub: https://github.com/GauriSP10/streamlit_login_auth_ui












