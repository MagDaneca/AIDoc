from cryptography.fernet import Fernet

key = b'5YFwBUgWOJ7dUscgnfTK0LH3R7mNP-l4MXGauZVOW70='

cipher_suite = Fernet(key)

def encrypt_data(data):
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def decrypt_data(encrypted_data):
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
        return decrypted_data
    except Exception as e:
        return None