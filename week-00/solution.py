def run_length_encode(s: str) -> list[tuple[str, int]]:
    if not s:
        return []
    result = []
    current, count = s[0], 1
    for ch in s[1:]:
        if ch == current:
            count += 1
        else:
            result.append((current, count))
            current, count = ch, 1
    result.append((current, count))
    return result
