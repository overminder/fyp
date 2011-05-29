
from hashlib import md5

def hash_digest(u_str):
    hasher = md5()
    hasher.update(u_str)
    return hasher.hexdigest()
