def generate_candidates(first: str, last: str, domain: str) -> list[str]:
    f = first.lower().strip()
    l = last.lower().strip()
    d = domain.lower().strip()
    return [
        f"{f}.{l}@{d}",
        f"{f}{l}@{d}",
        f"{f[0]}{l}@{d}",
        f"{f[0]}.{l}@{d}",
        f"{f}@{d}",
        f"{l}@{d}",
        f"{f}_{l}@{d}",
        f"recruiting@{d}",
        f"careers@{d}",
        f"talent@{d}",
        f"hr@{d}",
    ]
