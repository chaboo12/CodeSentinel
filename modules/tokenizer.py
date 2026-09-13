import re

def tokenize(code):

    code = re.sub(r'#.*', '', code)

    tokens = re.findall(
        r'[A-Za-z_][A-Za-z0-9_]*|[{}();,+\-*/]',
        code
    )

    return tokens 