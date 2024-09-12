from passlib.context import CryptContext

# Initialize the password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Password to hash
password = "1234"

# Hash the password twice
hashed_password1 = get_password_hash(password)
hashed_password2 = get_password_hash(password)

# Verify if the password matches the first hash
verification1 = verify_password(password, hashed_password1)
verification2 = verify_password(password, hashed_password2)

# Output the results
print("Hash 1:", hashed_password1)
print("Hash 2:", hashed_password2)
print("Verification of Hash 1:", verification1)  # Should print True
print("Verification of Hash 2:", verification2)  # Should print True
