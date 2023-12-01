import hashlib
import secrets
import string
import os

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 25
SPECIAL_CHAR = "!@#$%^&*"

def hash_pw(plain_text, salt='') -> str:
    """
    Generate hash of plain text. Here we allow for passing in a salt
    explicitly. This is so you can tinker and see the results.

    Python's Hashlib provides all we need here. Documentation is at
    https://docs.python.org/3/library/hashlib.html.

    Here we use SHA-1. (Weak!) For stronger encryption, see: bcrypt,
    scrypt, or Argon2. Nevertheless, this code should suffice for an
    introduction to some important concepts and practices.

    A few things to note.

    If we supply a fixed salt (or don't use a salt at all), then the
    output of the hash function becomes predictable -- for a given
    algorithm, the same password will always produce the same result.

    If we allow our algorithm to generate a salt from a pseudorandom
    input (e.g., using os.urandom(60)) then the same password will
    produce different results. All we know is the length of the combined
    salt and password.

    If we wish to be able to authenticate, then we must store the salt
    with the hash. We facilitate this by prepending the salt to the hash.

    :param plain_text: str (user-supplied password)
    :param salt: str
    :return: str (ASCII-encoded salt + hash)
    """
    # generate a len 80 hexadecimal value of bytes
    salt = os.urandom(40).hex()
    hashable = salt + plain_text  # concatenate salt and plain_text
    hashable = hashable.encode('utf-8')  # convert to bytes
    this_hash = hashlib.sha1(hashable).hexdigest()  # hash w/ SHA-1 and hexdigest
    return salt + this_hash # prepend hash and return


def authenticate(stored, plain_text, salt_length=None) -> bool:
    """
    Authenticate by comparing stored and new hashes.

    :param stored: str (salt + hash retrieved from database)
    :param plain_text: str (user-supplied password)
    :param salt_length: int
    :return: bool
    """
    salt_length = salt_length or 40  # set salt_length
    # multiply salt_length by 2 to match hexadecimal value
    salt_length*=2
    salt = stored[:salt_length]  # extract salt from stored value
    stored_hash = stored[salt_length:]  # extract hash from stored value
    hashable = salt + plain_text  # concatenate hash and plain text
    hashable = hashable.encode('utf-8')  # convert to bytes
    this_hash = hashlib.sha1(hashable).hexdigest()  # hash and digest
    return this_hash == stored_hash  # compare

def password_strength(test_password) -> bool:
    """
    Check basic password strength. Return true if password
    meets minimum complexity criteria, false otherwise.

    :param test_password: str
    :return: bool
    """
    if test_password.isalnum() or test_password.isalpha():
        return False
    if len(test_password) < PASSWORD_MIN_LENGTH:
        return False
    if len(test_password) > PASSWORD_MAX_LENGTH:
        return False
    special_char_check = False
    has_upper = False
    has_lower = False
    has_digit = False
    for ch in test_password:
        if ch in SPECIAL_CHAR:
            special_char_check = True
        if ch.isupper():
            has_upper = True
        if ch.islower():
            has_lower = True
        if ch.isdigit():
            has_digit = True
    if not special_char_check or \
            not has_upper or \
            not has_lower or \
            not has_digit:
        return False
    else:
        return True

def generate_password() -> str:
    """
    Generates a random password which passes all of the complexity requirements
    
    :return: str
    """
    # Random length between 8 and 25
    length = secrets.choice(range(PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH+1))
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special_characters = SPECIAL_CHAR

    # Ensure at least one character from each category
    password = (
        secrets.choice(lowercase) +
        secrets.choice(uppercase) +
        secrets.choice(digits) +
        secrets.choice(special_characters)
    )

    # Fill the remaining length with random characters
    remaining_chars = length - 4
    charset = lowercase + uppercase + digits + special_characters
    password += ''.join(secrets.choice(charset) for _ in range(remaining_chars))

    # Shuffle the password to ensure random order of characters
    password_list = list(password)
    secrets.SystemRandom().shuffle(password_list)
    return ''.join(password_list)