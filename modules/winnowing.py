import hashlib

def get_hashes(text, k=5):
    words = text.split()
    hashes = []

    for i in range(len(words) - k + 1):
        window = " ".join(words[i:i+k])
        h = hashlib.md5(window.encode()).hexdigest()
        hashes.append(h)

    return set(hashes)


def winnowing_similarity(a, b):
    h1 = get_hashes(a)
    h2 = get_hashes(b)

    if not h1 or not h2:
        return 0

    return round(len(h1 & h2) / len(h1 | h2) * 100, 2)