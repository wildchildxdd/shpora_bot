from texts import TEST_TEXT


def get_parts(symbol_capacity, text):
    parts = []
    text_len = len(text)
    chunks = text_len / symbol_capacity
    if chunks > int(chunks):
        chunks = int(chunks +1)
    for i in range(chunks):
        part = i + 1
        chunk = text[symbol_capacity*(part - 1):symbol_capacity*part]
        parts.append(f'{part}:\n{chunk}')
    return parts
