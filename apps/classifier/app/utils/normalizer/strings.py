import unicodedata

def normalize_string_utf8_to_ascii(string: str) -> str:
    return unicodedata.normalize('NFKD', string).encode('ascii', 'ignore').decode('ascii')
