import string
import random

def generate_password(password_length, uppercase_min, lowercase_min, digit_min, special_char_min):
    """
        Generates a strong, random password based on the specified minimum character counts and length.
    """
    characters = ""
    total_min = uppercase_min + lowercase_min + digit_min + special_char_min
    if total_min > password_length:
        raise ValueError("The total minimum number of characters exceeds the desired password length.")

    # Character set with the minimum required characters
    characters += string.ascii_uppercase[:uppercase_min]
    characters += string.ascii_lowercase[:lowercase_min]
    characters += string.digits[:digit_min]
    characters += string.punctuation[:special_char_min]

    # Fill the remaining length with random characters from the available character sets
    remaining_length = password_length - total_min
    if remaining_length > 0:
        remaining_uppercase = string.ascii_uppercase[uppercase_min:]
        remaining_lowercase = string.ascii_lowercase[lowercase_min:]
        remaining_digits = string.digits[digit_min:]
        remaining_special_chars = string.punctuation[special_char_min:]
        remaining_characters = remaining_uppercase + remaining_lowercase + remaining_digits + remaining_special_chars
        characters += ''.join(random.sample(remaining_characters, remaining_length))

    password = ''.join(random.sample(characters, password_length))
    return password

# User input for password length and minimum character counts
password_length = int(input("Enter the desired password length: "))
uppercase_min = int(input("Enter the minimum number of uppercase letters to include: "))
lowercase_min = int(input("Enter the minimum number of lowercase letters to include: "))
digit_min = int(input("Enter the minimum number of digits to include: "))
special_char_min = int(input("Enter the minimum number of special characters to include: "))

try:
    # Generate the password
    password = generate_password(password_length, uppercase_min, lowercase_min, digit_min, special_char_min)
    print("Generated password:", password)

except Exception as e:
    print("Error:", e)
