import string
import random


def generate_otp(length=6, whitelist=None, blacklist=None):
    """
    Generates a strong, One-Time Password (OTP) based on specified length, whitelist, and blacklist.
    """
    if length > 10:
        raise ValueError("Length must be 10 or less since there are only 10 unique digits.")
    elif length < 1:
        raise ValueError("OTP length must be at least 1.")

    # Create a list of digits based on whitelist and blacklist
    digits = list(string.digits)
    if whitelist:
        digits = [d for d in whitelist if d in digits]
    if blacklist:
        digits = [d for d in digits if d not in blacklist]

    if len(digits) < length:
        raise ValueError("Not enough unique digits available after applying whitelist and blacklist.")

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

    # User input for whitelist and blacklist
    whitelist_input = input("Enter allowed digits (whitelist) as a string (e.g., '13579'): ")
    blacklist_input = input("Enter disallowed digits (blacklist) as a string (e.g., '02468'): ")

    whitelist = list(whitelist_input) if whitelist_input else None
    blacklist = list(blacklist_input) if blacklist_input else None

    # Generate the OTP in desired length with whitelist and blacklist
    otp = generate_otp(otp_length, whitelist, blacklist)
    print("Your OTP is:", otp)

    # Generate a fixed 6-digit OTP
    otp_fixed = generate_otp(6, whitelist, blacklist)
    print("Your 6-digit OTP is:", otp_fixed)

except Exception as e:
    print("Error:", e)
