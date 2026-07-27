"""
Task 3: Password Generator
Generates strong, random passwords based on user-specified length and complexity.
"""

import random
import string


def generate_password(length, use_upper=True, use_digits=True, use_symbols=True):
    """Generate a random password of the given length using the selected character sets."""
    characters = string.ascii_lowercase

    if use_upper:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    password = "".join(random.choice(characters) for _ in range(length))
    return password


def get_positive_int(prompt):
    """Keep asking until the user enters a valid positive integer."""
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                print("Please enter a number greater than 0.")
                continue
            return value
        except ValueError:
            print("That's not a valid number. Try again.")


def get_yes_no(prompt):
    """Keep asking until the user enters y or n."""
    while True:
        choice = input(prompt).strip().lower()
        if choice in ("y", "yes"):
            return True
        if choice in ("n", "no"):
            return False
        print("Please enter 'y' or 'n'.")


def main():
    print("=== Password Generator ===\n")

    # User Input
    length = get_positive_int("Enter desired password length: ")
    use_upper = get_yes_no("Include uppercase letters? (y/n): ")
    use_digits = get_yes_no("Include numbers? (y/n): ")
    use_symbols = get_yes_no("Include symbols? (y/n): ")

    # Generate Password
    password = generate_password(length, use_upper, use_digits, use_symbols)

    # Display the Password
    print("\nYour generated password is:")
    print(password)


if __name__ == "__main__":
    main()