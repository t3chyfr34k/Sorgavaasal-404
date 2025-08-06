import re

TOKEN_REGEX = [
    ('NUMBER',    r'\d+'),
    ('IDENT',     r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('ASSIGN',    r'='),
    ('PLUS',      r'\+'),
    ('LPAREN',    r'\('),
    ('RPAREN',    r'\)'),
    ('LBRACE',    r'\{'),
    ('RBRACE',    r'\}'),
    ('SEMICOLON', r';'),
    ('NEWLINE',   r'\n'),
    ('SKIP',      r'[ \t]+'),
]

KEYWORDS = {
    'kooptaVaran': 'FUNCTION',
    'numberuu': 'NUMBER_TYPE',
    'Vandhutann': 'RETURN',
}

def tokenize(code):
    tokens = []
    pos = 0
    while pos < len(code):
        match = None
        for token_type, pattern in TOKEN_REGEX:
            regex = re.compile(pattern)
            match = regex.match(code, pos)
            if match:
                text = match.group(0)
                if token_type == 'IDENT' and text in KEYWORDS:
                    tokens.append((KEYWORDS[text], text))
                elif token_type != 'SKIP' and token_type != 'NEWLINE':
                    tokens.append((token_type, text))
                pos = match.end(0)
                break
        if not match:
            raise SyntaxError(f"Unexpected character: {code[pos]}")
    return tokens
