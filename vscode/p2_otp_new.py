# import string
# import random
#
# def generate_otp(length=6):
#     """
#     Generates a strong, 6-digit One-Time Password (OTP) without repeating digits and without consecutive digits.
#     """
#     digits = list(string.digits)
#     random.shuffle(digits)
#     otp=''
#     for i in range(length):
#         digit = random.choice(digits)
#         if otp and int(digit) == int(otp[-1]) + 1:
#             continue  # Skip consecutive digits
#         otp += digit
#         digits.remove(digit)
#     return otp
#
#
# # # User input for OTP length
# # otp_length = int(input("Enter the desired otp length: "))
#
# # try:
# #     # # Generate the OTP in desired length
# #     # otp = generate_otp(otp_length)
# #     # print("Your OTP is:", otp)
#
# # Generate the OTP in fixed length
# otp = generate_otp()
# print("Your 6-digit OTP is:", otp)
#
# # except Exception as e:
# #     print("Error:", e)

import string
import random

def generate_otp(length=6):
    """
    Generates a strong, 6-digit One-Time Password (OTP) without repeating digits and without consecutive digits.
    """
    if length > 10:
        raise ValueError("Length must be 10 or less since there are only 10 unique digits.")
    digits = list(string.digits)
    otp = ''
    while len(otp) < length:
        digit = random.choice(digits)
        # Check for consecutive digits
        if otp and abs(int(digit) - int(otp[-1])) == 1:
            continue  # Skip consecutive digits
        otp += digit
        digits.remove(digit)
    return otp


# Generate the OTP in fixed length
otp = generate_otp()
print("Your 6-digit OTP is:", otp)
