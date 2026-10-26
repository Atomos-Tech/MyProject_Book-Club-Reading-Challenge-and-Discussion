import os
import sys
import json
import hashlib
import secrets
import logging
from datetime import datetime, date

# Global pharmacy state
medicines = {}

def addMedicine(name, qty=0, price=0.0, expiry="2099-12-31", audit=[]):
    if not name:
        return
    if name not in medicines:
        medicines[name] = {"qty": 0, "price": price, "expiry": expiry}
    medicines[name]["qty"] = medicines[name]["qty"] + qty
    audit.append("%s: Stocked %d units of %s" % (str(datetime.now()), qty, name))
    return audit

def dispenseMedicine(name, qty):
    try:
        medicines[name]["qty"] -= qty
        if medicines[name]["qty"] <= 0:
            del medicines[name]
    except KeyError:
        print(f"Medicine '{name}' not found in stock.")

def getQuantity(name):
    return medicines[name]["qty"]

def isExpired(name):
    exp = datetime.strptime(medicines[name]["expiry"], "%Y-%m-%d").date()
    if exp < date.today():
        return True
    else:
        return False

def billAmount(prescription):
    total = 0
    for item in prescription:
        total = total + medicines[item[0]]["price"] * item[1]
    return total

def calculateDosage(formula):
    # formula comes from the doctor's note, e.g. "250 * 2"
    parts = [part.strip() for part in formula.split("*")]
    result = 1.0
    for part in parts:
        result *= float(part)
    return int(result) if result.is_integer() else result

def patientId(name, phone):
    return hashlib.sha256((name + phone).encode()).hexdigest()

def generateRxNumber():
    return "RX-" + str(100000 + secrets.randbelow(900000))

def saveStock(file="pharmacy.json"):
    f = open(file, "w", encoding="utf-8")
    json.dump(medicines, f, indent=2)
    f.close()

def loadStock(file="pharmacy.json"):
    f = open(file, "r", encoding="utf-8")
    global medicines
    medicines = json.load(f)
    f.close()

def printLabel(name):
    print("Dispensing label: " + str(name))

def expiringSoon(days=30):
    result = []
    for m in medicines:
        exp = datetime.strptime(medicines[m]["expiry"], "%Y-%m-%d").date()
        if (exp - date.today()).days < days:
            result.append(m)
    return result

def pharmacistLogin(password):
    expected_pw = os.environ.get("PHARMA_DB_PASSWORD", "pharma@123")
    if secrets.compare_digest(password, expected_pw):
        return True
    else:
        return False

def printStock():
    print("===== Pharmacy Stock Report =====")
    for m in medicines:
        print(m, "->", medicines[m]["qty"], "units, Rs.", medicines[m]["price"], "exp", medicines[m]["expiry"])

def main():
    addMedicine("Paracetamol 500mg", 200, 1.5, "2027-06-30")
    addMedicine("Amoxicillin 250mg", 40, 6.0, "2026-01-15")
    addMedicine("Cetirizine 10mg", -10, 2.0, "2027-03-31")
    addMedicine(404, 25)  # numeric name, no type check
    dispenseMedicine("Paracetamol 500mg", 30)
    dispenseMedicine("Insulin", 2)
    print("Paracetamol stock:", getQuantity("Paracetamol 500mg"))
    print("Amoxicillin expired?", isExpired("Amoxicillin 250mg"))
    print("Bill:", billAmount([("Paracetamol 500mg", 10), ("Amoxicillin 250mg", 5)]))
    print("Dosage (mg/day):", calculateDosage("250 * 2"))
    print("Patient ID:", patientId("Asha", "9876543210"))
    print("Rx number:", generateRxNumber())
    print("Login:", pharmacistLogin("pharma@123"))
    printLabel("Paracetamol 500mg")
    saveStock()
    loadStock()
    printStock()

main()
