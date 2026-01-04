import re
import math
import string
from getpass import getpass

def load_common_passwords():
    try:
        with open("common_passwords.txt", "r") as f:
            return set(p.strip() for p in f)
    except:
        return set()

COMMON_PASSWORDS = load_common_passwords()

def calculate_entropy(password):
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"[0-9]", password): pool += 10
    if re.search(rf"[{string.punctuation}]", password):
        pool += len(string.punctuation)

    return round(len(password) * math.log2(pool), 2) if pool else 0

def brute_force_time(entropy):
    guesses_per_sec = 1e9
    seconds = (2 ** entropy) / guesses_per_sec
    return seconds / (60 * 60 * 24 * 365)

def analyze_password(password):
    feedback = []
    score = 0

    if len(password) >= 12: score += 2
    else: feedback.append("Use at least 12 characters.")

    checks = {
        "lowercase": r"[a-z]",
        "uppercase": r"[A-Z]",
        "digit": r"[0-9]",
        "special": rf"[{string.punctuation}]"
    }

    for name, pattern in checks.items():
        if re.search(pattern, password): score += 1
        else: feedback.append(f"Add {name} characters.")

    if password.lower() in COMMON_PASSWORDS:
        feedback.append("Password found in common password list.")

    if re.search(r"(.)\1{2,}", password):
        feedback.append("Avoid repeated characters.")

    entropy = calculate_entropy(password)

    strength = "Strong" if score >= 6 and entropy >= 60 else "Moderate" if score >= 4 else "Weak"

    return strength, entropy, feedback, brute_force_time(entropy)

def main():
    print("\n🔐 Password Strength Analyzer 🔐")
    pwd = getpass("Enter password: ")

    strength, entropy, feedback, years = analyze_password(pwd)

    print(f"\nStrength: {strength}")
    print(f"Entropy: {entropy} bits")
    print(f"Estimated brute-force time: {years:.2f} years")

    if feedback:
        print("\nSuggestions:")
        for f in feedback:
            print("•", f)

if __name__ == "__main__":
    main()
