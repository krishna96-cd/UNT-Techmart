import secrets

# Generate a secure secret key
secret_key = secrets.token_hex(16)

print("Your generated secret key:", secret_key)
