import secrets
import string

def generate_verification_token():
    """Generate a secure verification token"""
    alphabet = string.ascii_letters + string.digits + "_-"
    return ''.join(secrets.choice(alphabet) for _ in range(50))

# Generate and save your token
token = generate_verification_token()
print(f"Your verification token: {token}")

