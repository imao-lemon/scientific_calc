"""Console-based Scientific Calculator.

Operations
----------
Binary : add, subtract, multiply, divide, power, modulus
Unary  : square root, factorial, sin, cos, tan (degrees),
         log10, natural log, absolute value

All operations raise CalculatorError for invalid input or undefined results,
so the menu loop (and the tests) can handle failures in one place.
"""

import math

MAX_FACTORIAL = 500  # keeps output readable and computation fast


class CalculatorError(Exception):
    """Raised for invalid input or mathematically undefined operations."""


# --------------------------------------------------------------------------
# Operations
# --------------------------------------------------------------------------
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise CalculatorError("Division by zero is undefined.")
    return a / b


def modulus(a, b):
    if b == 0:
        raise CalculatorError("Modulus by zero is undefined.")
    return a % b


def power(a, b):
    if a == 0 and b < 0:
        raise CalculatorError("0 cannot be raised to a negative power.")
    if a < 0 and not float(b).is_integer():
        raise CalculatorError(
            "A negative base with a fractional exponent has no real result."
        )
    try:
        return float(a) ** float(b)
    except OverflowError:
        raise CalculatorError("Result is too large to represent.")


def square_root(x):
    if x < 0:
        raise CalculatorError("Square root of a negative number is not real.")
    return math.sqrt(x)


def factorial(x):
    if not float(x).is_integer():
        raise CalculatorError("Factorial is defined only for whole numbers.")
    if x < 0:
        raise CalculatorError("Factorial is not defined for negative numbers.")
    if x > MAX_FACTORIAL:
        raise CalculatorError(f"Input too large (maximum is {MAX_FACTORIAL}).")
    return math.factorial(int(x))


def sine(x_deg):
    return math.sin(math.radians(x_deg))


def cosine(x_deg):
    return math.cos(math.radians(x_deg))


def tangent(x_deg):
    # tan is undefined at 90, 270, ... degrees
    if abs(math.cos(math.radians(x_deg))) < 1e-12:
        raise CalculatorError("Tangent is undefined at this angle.")
    return math.tan(math.radians(x_deg))


def log10(x):
    if x <= 0:
        raise CalculatorError("Logarithm is defined only for positive numbers.")
    return math.log10(x)


def natural_log(x):
    if x <= 0:
        raise CalculatorError("Logarithm is defined only for positive numbers.")
    return math.log(x)


def absolute(x):
    return abs(x)


# --------------------------------------------------------------------------
# Menu table: key -> (label, function, number of operands)
# --------------------------------------------------------------------------
OPERATIONS = {
    "1": ("Addition (a + b)", add, 2),
    "2": ("Subtraction (a - b)", subtract, 2),
    "3": ("Multiplication (a * b)", multiply, 2),
    "4": ("Division (a / b)", divide, 2),
    "5": ("Power (a ^ b)", power, 2),
    "6": ("Modulus (a % b)", modulus, 2),
    "7": ("Square root", square_root, 1),
    "8": ("Factorial (n!)", factorial, 1),
    "9": ("Sine (degrees)", sine, 1),
    "10": ("Cosine (degrees)", cosine, 1),
    "11": ("Tangent (degrees)", tangent, 1),
    "12": ("Log base 10", log10, 1),
    "13": ("Natural log (ln)", natural_log, 1),
    "14": ("Absolute value", absolute, 1),
}


# --------------------------------------------------------------------------
# Input / output helpers
# --------------------------------------------------------------------------
def parse_number(text):
    """Convert text to a float; raise CalculatorError if not a finite number."""
    try:
        value = float(text.strip())
    except ValueError:
        raise CalculatorError(f"'{text}' is not a valid number.")
    if math.isnan(value) or math.isinf(value):
        raise CalculatorError("Please enter a finite number.")
    return value


def read_number(prompt):
    """Keep asking until the user enters a valid number."""
    while True:
        try:
            return parse_number(input(prompt))
        except CalculatorError as err:
            print(f"  Error: {err}")


def format_result(value):
    """Show whole-number results without a trailing .0."""
    if isinstance(value, int):
        return str(value)
    if float(value).is_integer() and abs(value) < 1e15:
        return str(int(value))
    return f"{value:.10g}"


def calculate(choice, *operands):
    """Run the chosen operation. Raises CalculatorError on bad input."""
    if choice not in OPERATIONS:
        raise CalculatorError("Invalid menu choice.")
    _, func, arity = OPERATIONS[choice]
    if len(operands) != arity:
        raise CalculatorError(f"This operation needs {arity} number(s).")
    return func(*operands)


def show_menu():
    print("\n=== Scientific Calculator ===")
    for key, (label, _, _) in OPERATIONS.items():
        print(f"{key:>3}. {label}")
    print("  0. Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an operation: ").strip()

        if choice == "0":
            print("Goodbye!")
            break
        if choice not in OPERATIONS:
            print("  Error: please choose a number from the menu.")
            continue

        label, _, arity = OPERATIONS[choice]
        print(f"\n{label}")
        operands = [read_number("  Enter number: ") if arity == 1
                    else read_number(f"  Enter {name} number: ")
                    for name in (["first", "second"] if arity == 2 else [None])]

        try:
            result = calculate(choice, *operands)
            print(f"  Result: {format_result(result)}")
        except CalculatorError as err:
            print(f"  Error: {err}")

        again = input("\nAnother calculation? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()