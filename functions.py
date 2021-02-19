import random, sys, string, pyperclip
from cryptography.fernet import Fernet
import pyinputplus as pyip
from hashlib import sha256
from db_manager import *


def master():
    web = 'master'
    name = 'master'
    master_password = input('Enter master password: ')

    try:
        new_master_password = sha256(master_password.encode('utf-8')).hexdigest()
        save(web, name, new_master_password)
        print('Master password created!')
    except mysql.connector.errors.IntegrityError:
        hash_input = sha256(master_password.encode('utf-8')).hexdigest()
        master_password_hash = retrieve(web, name)
        if hash_input == master_password_hash:
            print('Access Granted!')
        else:
            print('Access Denied!')
            sys.exit()


def operation_list():
    operations = ('Save Password', 'Retrieve Password', 'Quit')
    print('-' * 50)
    print('Select any operation below:')
    for i, operation in enumerate(operations):
        print(f'{i + 1}. {operation}')


def generate_password(pass_length):
    symbol = '()~!@#$%^&*-_=+[{}]\/?'
    letters = string.ascii_letters + string.digits + symbol
    password = ''.join(random.sample(letters, pass_length - 1))
    password = password + random.choice(symbol)
    password_enc = encrypt_password(password)
    return password, password_enc


def encrypt_password(password):
    try:
        with open('key.key', 'rb') as k:
            key = k.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open('key.key', 'wb') as k:
            k.write(key)
    finally:
        fernet = Fernet(key)
        password_enc = fernet.encrypt(bytes(password, 'utf-8'))
        return password_enc


def decrypt_password(password):
    with open('key.key', 'rb') as k:
        key = k.read()
        fernet = Fernet(key)
        dec = fernet.decrypt(bytes(password, 'utf-8')).decode()
        return dec


def save_password():
    inside = True
    print('-' * 50)
    website = input("Please enter website's name: ")
    username = input("Enter email/username: ")
    if website != 'master' and username != 'master':
        print('-' * 50)
        print('Which one would you like: ')
        print('1. Generate random password')
        print('2. Save your own password')
        while inside:
            choice = input('Your choice: ')

            if choice == '1':
                while True:
                    pass_length = pyip.inputNum('Password length: ')
                    if 8 <= pass_length <= 16:
                        password, password_enc = generate_password(pass_length)
                        try:
                            save(website, username, password_enc)
                            pyperclip.copy(password)
                            print('Password saved and copied to clipboard!')
                        except mysql.connector.errors.IntegrityError:
                            print(f"{website.capitalize()}'s password for {username} already saved!")
                        inside = False
                        break
                    else:
                        print('Password length must be between 8 and 16')
                        continue

            elif choice == '2':
                while True:
                    password = input("Enter password to save: ")
                    if 8 <= len(password) <= 16:
                        password_enc = encrypt_password(password)
                        try:
                            save(website, username, password_enc)
                            pyperclip.copy(password)
                            print('Password saved and copied to clipboard!')
                        except mysql.connector.errors.IntegrityError:
                            print(f"{website.capitalize()}'s password for {username} already saved!")
                        inside = False
                        break
                    else:
                        print('Password length must be between 8 and 16')
                        continue
            else:
                print('Invalid choice!')
                continue
    else:
        print('Invalid website and username!')


def retrieve_password():
    website = input("Please enter website's name: ")
    username = input("Enter email/username: ")
    if website != 'master' and username != 'master':
        password_enc = retrieve(website, username)
        try:
            password = decrypt_password(password_enc)
            print(f'Your password is {password}')
            pyperclip.copy(password)
            print('Password copied to clipboard!')
        except TypeError:
            print('There is no data!')
    else:
        print('There is no data')
