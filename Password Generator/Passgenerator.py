import random
import string

def gen_strong_pass(length: int = 12):
    if length < 4:
        raise ValueError("Password length must be at least 4 to include all character types.")

    # Character groups
    lower = random.choice(string.ascii_lowercase)
    upper = random.choice(string.ascii_uppercase)
    digit = random.choice(string.digits)      
    symbol = random.choice(string.punctuation)

    # Fill the rest with random mix
    remaining = [random.choice(string.ascii_letters + string.digits + string.punctuation) 
                 for _ in range(length - 4)]

    # Combine all characters
    password_list = list(lower + upper + digit + symbol + ''.join(remaining))

    # Shuffle so the first 4 aren't predictable
    random.shuffle(password_list)

    # Join into string
    return ''.join(password_list)

Password = gen_strong_pass(12)
print(f"Generated Strong Password: {Password}")
