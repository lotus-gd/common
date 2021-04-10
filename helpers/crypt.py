import bcrypt

def bcrypt_hash(passw: str, difficulty: int = 10) -> str:
    """Hashes the pasword `passw` using the BCrypt hashing algorhythm.
    Args:
        passw (str): The password that is supposed to be hashed.
        difficulty (int): The amount of times the password should be salted
            (higher is more secure but slower).
    
    Returns:
        A string of the BCript hashed passwd.
    """

    return bcrypt.hashpw(
        passw.encode(),
        bcrypt.gensalt(difficulty)
    ).decode()

def bcrypt_check(plain_pass: str, bcrypt_pass: str) -> bool:
    """Compares a plain text password `plain_pass` to the BCrypt hashed
    password `bcrypt_pass`.
    
    Args:
        plain_pass (str): The plain text password to be compared to the BCrypt
            hashed one.
        bcrypt_pass (str): The BCrypt hashed password to be checked against
            the plain text one.
    
    Returns:
        Bool relating to whether the passwords
            match or not.
    """

    # This will be placed within a try statement as
    # non-bcryptable values will cause errors here
    # and we want that to count as auth failures.
    try:
        return bcrypt.checkpw(
            plain_pass.encode(),
            bcrypt_pass.encode()
        )
    # Bad bcrypt_pass would raise ValueError
    except ValueError:
        return False
