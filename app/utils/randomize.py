
import random

from string import ascii_lowercase, digits, ascii_uppercase

def get_random_name(length=25):
    y = "".join(random.choice(ascii_lowercase + digits) for _ in range(length))
    return y