
import random
import string
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import requests

# # Email Account Details
# email_address = 'your_email_address'
# email_password = 'your_email_password'
#
# # SMS API Details
# sms_api_url = 'https://api.textlocal.in/send/'
# sms_api_key = 'your_sms_api_key'
# sms_sender_id = 'your_sms_sender_id'
def generate_password(length, uppercase_count, lowercase_count, digit_count, special_char_count):
    """
    Generates a strong, random password based on the specified character counts.

    Args:
        uppercase_count (int): The number of uppercase letters to include.
        lowercase_count (int): The number of lowercase letters to include.
        digit_count (int): The number of digits to include.
        special_char_count (int): The number of special characters to include.

    Returns:
        str: The generated password.
    """
    characters = ""
    # password_length = uppercase_count + lowercase_count + digit_count + special_char_count

    if uppercase_count > 0:
        characters += string.ascii_uppercase
    if lowercase_count > 0:
        characters += string.ascii_lowercase
    if digit_count > 0:
        characters += string.digits
    if special_char_count > 0:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Get user input for character counts


# # Generate the password
# password = generate_password(uppercase_count, lowercase_count, digit_count, special_char_count)
# print("Generated password:", password)

# def generate_password(length=8):
#     """Generate a password based on the password rules"""
#     characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
#     password = ''.join(random.choice(characters) for i in range(length))
#     return password

def generate_otp(length=6):
    """Generate a 6-digit OTP"""
    digits = string.digits
    otp = ''.join(random.choice(digits) for i in range(length))
    # otp=str(random.randint(100000, 999999))
    return otp

# def send_sms(otp, phone_number):
#     """Send OTP to user's mobile number using SMS API"""
#     data = {
#         'apikey': sms_api_key,
#         'sender': sms_sender_id,
#         'numbers': phone_number,
#         'message': f'Your OTP is: {otp}'
#     }
#     response = requests.post(sms_api_url, data=data)
#     print(f'SMS sent to {phone_number}', response)
#
# def send_email(otp, password, email_address):
#     """Send OTP and password to user's email address"""
#     msg = MIMEMultipart()
#     msg['From'] = email_address
#     msg['To'] = email_address
#     msg['Subject'] = 'OTP and Password'
#     body = f'Your OTP is: {otp}\nYour Password is: {password}'
#     msg.attach(MIMEText(body, 'plain'))
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(email_address, email_password)
#     text = msg.as_string()
#     server.sendmail(email_address, email_address, text)
#     server.quit()
#     print(f'Email sent to {email_address}')


password_length = int(input('Enter the password length (default is 8): ') or 8)
uppercase_count = int(input("Enter the number of uppercase letters to include: "))
lowercase_count = int(input("Enter the number of lowercase letters to include: "))
digit_count = int(input("Enter the number of digits to include: "))
special_char_count = int(input("Enter the number of special characters to include: "))
if password_length < 8:
    print('Password length should be at least 8 characters.')
else:
    password = generate_password(password_length,uppercase_count, lowercase_count, digit_count, special_char_count)
    otp = generate_otp()
    print(f'Generated Password: {password}')
    print(f'Generated OTP: {otp}')
    # phone_number = input('Enter user mobile number: ')
    # user_email = input('Enter user email address: ')
    # send_sms(otp, phone_number)
    # send_email(otp, password, user_email)


# import string
# import random
#
