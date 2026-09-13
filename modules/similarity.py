from difflib import SequenceMatcher
from modules.ast_analyzer import ast_similarity

def text_similarity(a, b):
    return SequenceMatcher(
        None,
        a,
        b
    ).ratio() * 100

def hybrid_similarity(a, b):

    text_score = text_similarity(a, b)

    ast_score = ast_similarity(
        a,
        b
    )

    final_score = (
        0.6 * text_score +
        0.4 * ast_score
    )

    return round(final_score, 2)

