import ast
from difflib import SequenceMatcher


def ast_similarity(code1, code2):

    try:
        tree1 = ast.dump(ast.parse(code1))
        tree2 = ast.dump(ast.parse(code2))

        return (
            SequenceMatcher(
                None,
                tree1,
                tree2
            ).ratio()
            * 100
        )

    except:
        return 0
    