import string
import random

def generate_otp(length=6):
    """
    Generates a strong, 6-digit One-Time Password (OTP) without repeating digits and without consecutive digits.
    """
    if length > 10:
        raise ValueError("Length must be 10 or less since there are only 10 unique digits.")
    elif length < 1:
        raise ValueError("OTP length must be at least 1.")
    else:
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

try:
    # User input for OTP length
    otp_length = int(input("Enter the desired OTP length: "))

    # Generate the OTP in desired length
    otp = generate_otp(otp_length)
    print("Your OTP is:", otp)

    # Generate a fixed 6-digit OTP
    otp_fixed = generate_otp()
    print("Your 6-digit OTP is:", otp_fixed)

except Exception as e:
    print("Error:", e)
