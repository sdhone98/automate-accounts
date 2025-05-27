import time
import random


def id_generator(prefix: str) -> str:
    if not prefix:
        raise ValueError("Prefix is required")
    if len(prefix) != 3:
        raise ValueError("Prefix must be exactly 3 characters long.")

    unix_time = int(time.time())
    random_digits = f"{random.randint(0, 9999):04d}"

    return f"{prefix}{unix_time}{random_digits}"
