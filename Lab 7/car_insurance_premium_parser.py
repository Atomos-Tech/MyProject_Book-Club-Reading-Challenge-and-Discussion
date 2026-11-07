import datetime


def normalize_registration(plate):
    """
    Removes spaces, dashes and dots from a registration number and upper-cases it.
    Returns None if plate is not a valid non-empty ASCII alphanumeric string.
    """
    if not isinstance(plate, str):
        return None
    cleaned = plate.strip()
    for ch in [' ', '-', '.']:
        cleaned = cleaned.replace(ch, '')
    if not cleaned or not cleaned.isascii() or not cleaned.isalnum():
        return None
    return cleaned.upper()


def total_claim_amount(text):
    """
    Adds up non-negative whole-number claim amounts separated by semicolons.
    Returns None if text is invalid or any amount is malformed.
    """
    if not isinstance(text, str) or not text.strip():
        return None
    parts = text.split(';')
    total = 0
    for part in parts:
        token = part.strip()
        if not token or not token.isascii() or not token.isdigit():
            return None
        total += int(token)
    return total


def driver_age(dob, current_year=2026):
    """
    Works out the driver's age from a DD/MM/YYYY date of birth.
    Returns None if dob is not a valid calendar date or produces an invalid age.
    """
    if not isinstance(dob, str) or not isinstance(current_year, int):
        return None
    parts = dob.strip().split('/')
    if len(parts) != 3:
        return None
    dd_str, mm_str, yyyy_str = parts
    if (
        len(yyyy_str) != 4
        or not (dd_str.isascii() and dd_str.isdigit())
        or not (mm_str.isascii() and mm_str.isdigit())
        or not (yyyy_str.isascii() and yyyy_str.isdigit())
    ):
        return None
    day, month, year = int(dd_str), int(mm_str), int(yyyy_str)
    try:
        datetime.date(year, month, day)
    except ValueError:
        return None
    age = current_year - year
    if age < 0 or age > 120:
        return None
    return age


def main():
    print("==== Running normalize_registration ====")
    value = input("Enter a registration number (e.g. ka 01 ab 1234): ")
    res = normalize_registration(value)
    print("Normalized registration:", res if res is not None else "Invalid input")

    print("\n==== Running total_claim_amount ====")
    value = input("Enter past claim amounts separated by ; (e.g. 12000;4500;800): ")
    res = total_claim_amount(value)
    print("Total claimed:", res if res is not None else "Invalid input")

    print("\n==== Running driver_age ====")
    value = input("Enter the driver's date of birth as DD/MM/YYYY (e.g. 14/08/1999): ")
    res = driver_age(value)
    print("Driver age in 2026:", res if res is not None else "Invalid input")


if __name__ == "__main__":
    main()
