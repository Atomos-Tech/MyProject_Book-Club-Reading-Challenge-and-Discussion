"""Pharmacy stock and billing management module."""
import os
import json
import hashlib
import secrets
from datetime import datetime, date

# Global pharmacy state
medicines = {}

def add_medicine(name, qty=0, price=0.0, expiry="2099-12-31", audit=None):
    """Add medicine stock after validating name, quantity, and price."""
    if audit is None:
        audit = []
    if not isinstance(name, str) or not name.strip():
        return audit
    if not isinstance(qty, int) or qty <= 0 or price < 0:
        return audit
    if name not in medicines:
        medicines[name] = {"qty": 0, "price": float(price), "expiry": expiry}
    medicines[name]["qty"] += qty
    audit.append(f"{datetime.now()}: Stocked {qty} units of {name}")
    return audit

def dispense_medicine(name, qty):
    """Dispense a specified quantity of medicine from stock."""
    if not isinstance(qty, int) or qty <= 0:
        return
    try:
        medicines[name]["qty"] -= qty
        if medicines[name]["qty"] <= 0:
            del medicines[name]
    except KeyError:
        print(f"Medicine '{name}' not found in stock.")

def get_quantity(name):
    """Return the available stock quantity for a medicine."""
    return medicines.get(name, {}).get("qty", 0)

def is_expired(name):
    """Check whether a medicine has passed its expiry date."""
    if name not in medicines:
        return False
    exp = datetime.strptime(medicines[name]["expiry"], "%Y-%m-%d").date()
    return exp < date.today()

def bill_amount(prescription):
    """Calculate total bill amount for a list of (medicine, qty) items."""
    total = 0.0
    for item_name, qty in prescription:
        if item_name in medicines and qty > 0:
            total += medicines[item_name]["price"] * qty
    return total

def calculate_dosage(formula):
    """Safely evaluate a dosage multiplication formula like '250 * 2'."""
    parts = [part.strip() for part in formula.split("*")]
    result = 1.0
    for part in parts:
        result *= float(part)
    return int(result) if result.is_integer() else result

def patient_id(name, phone):
    """Generate a SHA-256 hash identifier for a patient."""
    return hashlib.sha256((name + phone).encode()).hexdigest()

def generate_rx_number():
    """Generate a cryptographically random prescription number."""
    return f"RX-{100000 + secrets.randbelow(900000)}"

def save_stock(file_path="pharmacy.json"):
    """Save the current medicine stock dictionary to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file_handle:
        json.dump(medicines, file_handle, indent=2)

def load_stock(file_path="pharmacy.json"):
    """Load medicine stock data from a JSON file into memory."""
    with open(file_path, "r", encoding="utf-8") as file_handle:
        loaded_data = json.load(file_handle)
    medicines.clear()
    medicines.update(loaded_data)

def print_label(name):
    """Print a dispensing label for the given medicine."""
    print(f"Dispensing label: {name}")

def expiring_soon(days=30):
    """Return a list of medicines expiring within the given number of days."""
    result = []
    for med_name, details in medicines.items():
        exp = datetime.strptime(details["expiry"], "%Y-%m-%d").date()
        if (exp - date.today()).days < days:
            result.append(med_name)
    return result

def pharmacist_login(password):
    """Verify pharmacist login password against configured credentials."""
    expected_pw = os.environ.get("PHARMA_DB_PASSWORD", "pharma@123")
    return secrets.compare_digest(password, expected_pw)

def print_stock():
    """Display the current pharmacy stock report."""
    print("===== Pharmacy Stock Report =====")
    for med_name, details in medicines.items():
        print(f"{med_name} -> {details['qty']} units, Rs. {details['price']} exp {details['expiry']}")

def main():
    """Run a demonstration of the pharmacy management operations."""
    add_medicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    add_medicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    add_medicine("Cetirizine 10mg", -10, 2.0, "2027-03-31")
    add_medicine(404, 25)  # numeric name, rejected by type check
    dispense_medicine("Paracetamol 500mg", 30)
    dispense_medicine("Insulin", 2)
    print("Paracetamol stock:", get_quantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", is_expired("Amoxicillin 250mg"))
    print("Bill:", bill_amount([("Paracetamol 500mg", 10), ("Amoxicillin 250mg", 5)]))
    print("Dosage (mg/day):", calculate_dosage("250 * 2"))
    print("Patient ID:", patient_id("Asha", "9876543210"))
    print("Rx number:", generate_rx_number())
    print("Login:", pharmacist_login("pharma@123"))
    print_label("Paracetamol 500mg")
    save_stock()
    load_stock()
    print_stock()

if __name__ == "__main__":
    main()
