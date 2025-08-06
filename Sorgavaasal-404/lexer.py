import re

# Token Types
TOKEN_TYPES = {
    "NUMBER": r'\d+',
    "STRING": r'"[^"]*"',
    "IDENTIFIER": r'[a-zA-Z_]\w*',
    "KEYWORDS": [
        "irukuAanaIllaa", "thirumbaVaa", "oruvelaIrukumoo", "illanaPoo",
        "kooptaVarann", "paapomaa", "aiyoo", "kadasiyaa", "vandhutann",
        "jaamanSettuu", "irundha", "varaikum", "menja",
    ],
    "SYMBOLS": r'[\(\)\{\}=:,+\-*/<>]'
}

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}"

def lex(source):
    tokens = []
    pos = 0
    while pos < len(source):
        current = source[pos]

        if current.isspace():
            pos += 1
            continue

        if match := re.match(TOKEN_TYPES["NUMBER"], source[pos:]):
            tokens.append(Token("NUMBER", int(match.group())))
            pos += len(match.group())
        elif match := re.match(TOKEN_TYPES["STRING"], source[pos:]):
            tokens.append(Token("STRING", match.group()[1:-1]))
            pos += len(match.group())
        elif match := re.match(TOKEN_TYPES["IDENTIFIER"], source[pos:]):
            value = match.group()
            if value in TOKEN_TYPES["KEYWORDS"]:
                tokens.append(Token("KEYWORD", value))
            else:
                tokens.append(Token("IDENTIFIER", value))
            pos += len(match.group())
        elif match := re.match(TOKEN_TYPES["SYMBOLS"], current):
            tokens.append(Token("SYMBOL", current))
            pos += 1
        else:
            raise SyntaxError(f"Unknown character: {current}")

    return tokens
