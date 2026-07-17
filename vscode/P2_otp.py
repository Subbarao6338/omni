#1

import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client

# Twilio Account Details
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_phone_number = 'your_twilio_phone_number'

# Email Account Details
email_address = 'your_email_address'
email_password = 'your_email_password'

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_sms(otp, phone_number):
    """Send OTP to user's mobile number using Twilio"""
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f'Your OTP is: {otp}',
        from_=twilio_phone_number,
        to=phone_number
    )
    print(f'SMS sent to {phone_number}')

def send_email(otp, email_address):
    """Send OTP to user's email address"""
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = email_address
    msg['Subject'] = 'OTP for Authentication'
    body = f'Your OTP is: {otp}'
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    text = msg.as_string()
    server.sendmail(email_address, email_address, text)
    server.quit()
    print(f'Email sent to {email_address}')

def main():
    otp = generate_otp()
    phone_number = input('Enter user mobile number: ')
    user_email = input('Enter user email address: ')
    send_sms(otp, phone_number)
    send_email(otp, user_email)
    print(f'OTP: {otp}')

if __name__ == '__main__':
    main()


#2

import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

# Email Account Details
email_address = 'your_email_address'
email_password = 'your_email_password'

# SMS API Details
sms_api_url = 'https://api.textlocal.in/send/'
sms_api_key = 'your_sms_api_key'
sms_sender_id = 'your_sms_sender_id'

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_sms(otp, phone_number):
    """Send OTP to user's mobile number using SMS API"""
    data = {
        'apikey': sms_api_key,
        'sender': sms_sender_id,
        'numbers': phone_number,
        'message': f'Your OTP is: {otp}'
    }
    response = requests.post(sms_api_url, data=data)
    print(f'SMS sent to {phone_number}')

def send_email(otp, email_address):
    """Send OTP to user's email address"""
    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = email_address
    msg['Subject'] = 'OTP for Authentication'
    body = f'Your OTP is: {otp}'
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_address, email_password)
    text = msg.as_string()
    server.sendmail(email_address, email_address, text)
    server.quit()
    print(f'Email sent to {email_address}')

def main():
    otp = generate_otp()
    phone_number = input('Enter user mobile number: ')
    user_email = input('Enter user email address: ')
    send_sms(otp, phone_number)
    send_email(otp, user_email)
    print(f'OTP: {otp}')

if __name__ == '__main__':
    main()

#3

import random
import string

def generate_password(length=8):
    """Generate a password based on the password rules"""
    # Define the character sets
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = string.punctuation

    # Ensure the password contains at least one character from each set
    password = [
        random.choice(uppercase_letters),
        random.choice(lowercase_letters),
        random.choice(digits),
        random.choice(special_characters)
    ]

    # Fill the rest of the password with random characters
    for _ in range(length - 4):
        password.append(random.choice(
            uppercase_letters + lowercase_letters + digits + special_characters
        ))

    # Shuffle the password to avoid the first characters always being in the same character set
    random.shuffle(password)

    return ''.join(password)

def main():
    password_length = int(input('Enter the password length (default is 8): ') or 8)
    if password_length < 8:
        print('Password length should be at least 8 characters.')
    else:
        password = generate_password(password_length)
        print(f'Generated Password: {password}')

if __name__ == '__main__':
    main()


#4

import random
import string

def generate_password(length=8):
    """Generate a password based on the password rules"""
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def main():
    password_length = int(input('Enter the password length (default is 8): ') or 8)
    if password_length < 8:
        print('Password length should be at least 8 characters.')
    else:
        password = generate_password(password_length)
        print(f'Generated Password: {password}')

if __name__ == '__main__':
    main()


#5



#6

import random
import string

def generate_otp(length=6):
    """Generate a 6-digit OTP"""
    digits = string.digits
    otp = ''.join(random.choice(digits) for _ in range(length))
    return otp

def generate_strong_password(length=12):
    """Generate a strong password"""
    all_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(all_characters) for _ in range(length))
    return password

def main():
    print("Generated OTP: ", generate_otp())
    print("Generated Strong Password: ", generate_strong_password())

if __name__ == "__main__":
    main()


#7

import random
import secrets

otp = ''.join(str(random.randint(0, 9)) for _ in range(6))
password = ''.join(secrets.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()") for _ in range(12))

print("Generated OTP: ", otp)
print("Generated Strong Password: ", password)

