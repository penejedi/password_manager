import mysql.connector
from hashlib import sha256
import sys

db = mysql.connector.connect(
    host="localhost",
    user="youruser",
    password='yourpassword'
)

mycursor = db.cursor()
mycursor.execute('USE password')


def master():
    master_password = input('Enter master password: ')

    try:
        web = 'master'
        name = 'master'
        new_master_password = sha256((master_password).encode('utf-8')).hexdigest()
        save(web, name, new_master_password)
        print('Master password created!')
    except mysql.connector.errors.IntegrityError:
        hash_input = sha256((master_password).encode('utf-8')).hexdigest()
        mycursor.execute('SELECT password FROM password_data WHERE website="master" AND username="master"')
        for i in mycursor:
            global master_password_hash
            master_password_hash = i[0]
        if hash_input == master_password_hash:
            print('Acces Granted!')
        else:
            print('Access Denied!')
            sys.exit()


def save(website, username, password):
    mycursor.execute('INSERT INTO password_data (website, username, password) VALUES (%s,%s,%s)',
                     (website, username, password))
    db.commit()
