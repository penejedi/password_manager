import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password='Hanafi2096!'
)

cursor = db.cursor()
cursor.execute('CREATE DATABASE IF NOT EXISTS password_manager')
cursor.execute('USE password_manager')
cursor.execute('CREATE TABLE IF NOT EXISTS password_data ('
               '    website VARCHAR(50) NOT NULL,'
               '    username VARCHAR(50) NOT NULL,'
               '    password VARCHAR(100) NOT NULL,'
               'PRIMARY KEY (website, username))')


def save(website, username, password):
    cursor.execute('INSERT INTO password_data (website, username, password) VALUES (%s,%s,%s)',
                   (website, username, password))
    db.commit()


def retrieve(website, username):
    cursor.execute('SELECT password FROM password_data WHERE website=(%s) AND username=(%s)',
                   (website, username))
    password = cursor.fetchall()
    if len(password) == 1:
        return password[0][0]
