import hashlib
import getpass
import os
import hmac

# username -> {"salt": bytes, "hash": hex}
password_manager = {}

def hash_password(password: str, salt: bytes) -> str:
    return hashlib.sha256(salt + password.encode()).hexdigest()

def create_account():
    username = input("Enter your Username: ").strip()
    if username in password_manager:
        print("Username already exists.")
        return
    password = getpass.getpass("Enter your Password: ")
    salt = os.urandom(16)
    pwd_hash = hash_password(password, salt)
    password_manager[username] = {"salt": salt, "hash": pwd_hash}
    print("Account created successfully!")

def login():
    username = input("Enter your Username: ").strip()
    if username not in password_manager:
        print("Invalid username or password.")
        return
    password = getpass.getpass("Enter your Password: ")
    rec = password_manager[username]
    attempt = hash_password(password, rec["salt"])
    if hmac.compare_digest(attempt, rec["hash"]):
        print("Login successful")
    else:
        print("Invalid username or password.")

def main():
    while True:
        choice = input("Enter 1 to create an account, 2 to login or 0 to Exit: ").strip()
        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
