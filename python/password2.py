import random
import string
import json
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import threading
import time

class PasswordLogger:
    def __init__(self, log_file='password_log.json'):
        self.log_file = log_file
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    def log_password(self, password, is_strong):
        with open(self.log_file, 'r+') as f:
            data = json.load(f)
            data.append({'password': password, 'is_strong': is_strong})
            f.seek(0)
            json.dump(data, f)

class PasswordStrengthModel:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.is_trained = False

    def train(self, data):
        df = pd.DataFrame(data)
        X = df['password'].apply(self.extract_features).tolist()
        y = df['is_strong']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        self.model.fit(X_train, y_train)
        self.is_trained = True

    def extract_features(self, password):
        return [len(password), sum(c.isupper() for c in password), sum(c.isdigit() for c in password), sum(c in string.punctuation for c in password)]

    def predict_strength(self, password):
        if not self.is_trained:
            return False  # Not trained yet
        features = self.extract_features(password)
        return self.model.predict([features])[0]

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

def continuous_training(model, logger):
    while True:
        with open(logger.log_file, 'r') as f:
            data = json.load(f)
            if len(data) > 100:  # Retrain if we have enough data
                model.train(data)
        time.sleep(3600)  # Wait for an hour before checking again

def main():
    logger = PasswordLogger()
    model = PasswordStrengthModel()

    # Start continuous training in a separate thread
    training_thread = threading.Thread(target=continuous_training, args=(model, logger))
    training_thread.start()

    while True:
        print("\nPassword Generator")
        print("1. Generate Password")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            try:
                # User input for password length
                password_length = int(input("Enter the desired password length (min 6): "))
                # Check for minimum length immediately
                if password_length < 6:
                    print("Error: Password length must be at least 6 characters.")
                    continue  # Skip to the next iteration of the loop
                else:
                    # User input for minimum character counts
                    uppercase_min = int(input("Enter the minimum number of uppercase letters to include: "))
                    lowercase_min = int(input("Enter the minimum number of lowercase letters to include: "))
                    digit_min = int(input("Enter the minimum number of digits to include: "))
                    special_char_min = int(input("Enter the minimum number of special characters to include: "))

                    # Generate the password
                    password = generate_password(password_length, uppercase_min, lowercase_min, digit_min, special_char_min)
                    is_strong = model.predict_strength(password)
                    logger.log_password(password, is_strong)
                    print("Generated password:", password)
                    print("Is the password strong?", is_strong)

            except Exception as e:
                print("Error:", e)

        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
