import re
import string

# API keys use ascii_50 for the left and right halves
ascii_50 = "".join(set(string.ascii_letters + string.digits) - set("1IiLl0Oo5S8B"))
API_KEY_REGEX = re.compile(r"^[{}]+_[{}]+$".format(ascii_50, ascii_50))


def is_valid_api_key(api_key):
    if API_KEY_REGEX.match(api_key):
        return True
    return False
