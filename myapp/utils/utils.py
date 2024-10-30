import re
def createPostslug(text):
    # Replace any non-alphanumeric character (symbols, spaces, etc.) with a hyphen
    return re.sub(r'[^a-zA-Z0-9]', '-', text)

