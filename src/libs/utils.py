import hashlib


def generate_unique_id(title: str):
    # Create a unique ID by hashing the task title
    return hashlib.sha256(title.encode('utf-8')).hexdigest()
