import random
import string

def generate_password(length=12):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

new_password = generate_password()

with open("premium_password.txt", "w") as f:
    f.write(new_password)

print("🔐 New premium password generated and saved:", new_password)