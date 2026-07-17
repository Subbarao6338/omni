import string
import random

def generate_password(password_length, uppercase_min, lowercase_min, digit_min, special_char_min):
    """
    Generates a strong, random password based on the specified minimum character counts and length.
    """
    # Enforce a minimum password length of 6
    if password_length < 6:
        raise ValueError("Password length must be at least 6 characters.")

    total_min = uppercase_min + lowercase_min + digit_min + special_char_min
    if total_min > password_length:
        raise ValueError("The total minimum number of characters exceeds the desired password length.")

    # Validate minimum counts
    if (uppercase_min < 0 or lowercase_min < 0 or digit_min < 0 or special_char_min < 0):
        raise ValueError("Minimum counts cannot be negative.")

    # Initialize the password with the minimum required characters
    password_chars = []
    if uppercase_min > 0:
        password_chars += random.sample(string.ascii_uppercase, uppercase_min)
    if lowercase_min > 0:
        password_chars += random.sample(string.ascii_lowercase, lowercase_min)
    if digit_min > 0:
        password_chars += random.sample(string.digits, digit_min)
    if special_char_min > 0:
        password_chars += random.sample(string.punctuation, special_char_min)

    # Fill the remaining length with random characters from all available character sets
    remaining_length = password_length - len(password_chars)
    if remaining_length > 0:
        remaining_characters = ''
        if uppercase_min > 0:
            remaining_characters += string.ascii_uppercase
        if lowercase_min > 0:
            remaining_characters += string.ascii_lowercase
        if digit_min > 0:
            remaining_characters += string.digits
        if special_char_min > 0:
            remaining_characters += string.punctuation

        password_chars += random.choices(remaining_characters, k=remaining_length)

    # Shuffle the password characters to ensure randomness
    random.shuffle(password_chars)
    password = ''.join(password_chars)
    return password

try:
    # User input for password length
    password_length = int(input("Enter the desired password length (min 6): "))
    # Check for minimum length immediately
    if password_length < 6:
        print("Error: Password length must be at least 6 characters.")
        # continue  # Skip to the next iteration of the loop
    else:
        # User input for minimum character counts
        uppercase_min = int(input("Enter the minimum number of uppercase letters to include: "))
        lowercase_min = int(input("Enter the minimum number of lowercase letters to include: "))
        digit_min = int(input("Enter the minimum number of digits to include: "))
        special_char_min = int(input("Enter the minimum number of special characters to include: "))

        # Generate the password
        password = generate_password(password_length, uppercase_min, lowercase_min, digit_min, special_char_min)
        print("Generated password:", password)

except Exception as e:
    print("Error:", e)
