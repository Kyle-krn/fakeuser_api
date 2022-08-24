import string
import random
from typing import List

def generate_password(length: int, easy_to_read: bool = False, characters: List[str] = []):
    strings = ''

    punctuation = string.punctuation
    punctuation = punctuation.replace("'", "")
    punctuation = punctuation.replace('"', "")
    punctuation = punctuation.replace("\\", "")


    if "uppercase" in characters:
        strings += string.ascii_uppercase
    if "lowercase" in characters:
        strings += string.ascii_lowercase
    if "numbers" in characters:
        strings += string.digits
    if "symbols" in characters:
        strings += punctuation
    if strings == "":
        strings = string.ascii_uppercase + string.ascii_lowercase + string.digits + punctuation

    if easy_to_read:
        strings = strings.replace("l", "")
        strings = strings.replace("1", "")
        strings = strings.replace("o", "")
        strings = strings.replace("O", "")
        strings = strings.replace("0", "")
    
    return ''.join(random.choice(strings) for _ in range(length))
