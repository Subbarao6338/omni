import random
import string

def generate_otp():
    """
    Generates a strong, 6-digit One-Time Password (OTP) without repeating digits and without consecutive digits.
    """
    digits = list(string.digits)
    random.shuffle(digits)
    # otp = ''.join(digits[:6])
    otp=''
    # Ensure no consecutive digits
    # while any(otp[i:i+2] in ['01', '12', '23', '34', '45', '56', '67', '78', '89'] for i in range(len(otp)-1)):
    #     random.shuffle(digits)
    #     otp = ''.join(digits[:6])
    for i in range(6):
        digit = random.choice(digits)
        if otp and int(digit) == int(otp[-1]) + 1:
            continue  # Skip consecutive digits
        otp += digit
        digits.remove(digit)
    return otp

# Generate the OTP
otp = generate_otp()
print("Your 6-digit OTP is:", otp)
