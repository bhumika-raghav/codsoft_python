"""
Calculator Application
------------------------
A simple command-line calculator built with Python.
Prompts the user for two numbers and an operation, then performs
the calculation and displays the result.
"""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b


def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid number.\n")


def main():
    menu = """
========== CALCULATOR ==========
1. Add        (+)
2. Subtract   (-)
3. Multiply   (*)
4. Divide     (/)
5. Exit
=================================
"""
    while True:
        print(menu)
        choice = input("Choose an operation (1-5): ").strip()

        if choice == "5":
            print("Goodbye!")
            break

        if choice not in ("1", "2", "3", "4"):
            print("Invalid choice. Please choose 1-5.\n")
            continue

        num1 = get_number("Enter the first number: ")
        num2 = get_number("Enter the second number: ")

        if choice == "1":
            result = add(num1, num2)
            symbol = "+"
        elif choice == "2":
            result = subtract(num1, num2)
            symbol = "-"
        elif choice == "3":
            result = multiply(num1, num2)
            symbol = "*"
        elif choice == "4":
            result = divide(num1, num2)
            symbol = "/"

        print(f"\nResult: {num1} {symbol} {num2} = {result}\n")


if __name__ == "__main__":
    main()
