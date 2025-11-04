# isbn.py

def normalize_isbn(s: str) -> str:
    """
    Elimina espacios y guiones de la cadena y valida caracteres permitidos.
    Solo se permiten dígitos (y 'X' al final en ISBN-10).
    Retorna la cadena normalizada o cadena vacía si no es válida.
    """
    if not s or not isinstance(s, str):
        return ""

    s = s.replace(" ", "").replace("-", "").upper()

    if not s:
        return ""

    # Validar caracteres permitidos
    if not all(ch.isdigit() or ch == "X" for ch in s):
        return ""

    # 'X' solo puede estar al final en ISBN-10
    if "X" in s[:-1]:
        return ""

    return s


def is_valid_isbn10(s: str) -> bool:
    """
    Valida un ISBN-10 según la regla: sum( (10 - i) * d_i ) % 11 == 0
    donde 'X' representa el dígito 10 solo si está en la última posición.
    """
    s = normalize_isbn(s)
    if len(s) != 10:
        return False

    total = 0
    for i, ch in enumerate(s):
        if ch == "X":
            if i != 9:  # 'X' solo al final
                return False
            value = 10
        else:
            if not ch.isdigit():
                return False
            value = int(ch)
        total += (10 - i) * value

    return total % 11 == 0


def is_valid_isbn13(s: str) -> bool:
    """
    Valida un ISBN-13 según la regla: sum( d_i * peso ) % 10 == 0,
    con pesos alternos 1, 3.
    """
    s = normalize_isbn(s)
    if len(s) != 13 or not s.isdigit():
        return False

    total = 0
    for i, ch in enumerate(s):
        digit = int(ch)
        weight = 1 if i % 2 == 0 else 3
        total += digit * weight

    return total % 10 == 0


def detect_isbn(s: str) -> str:
    """
    Normaliza y detecta el tipo de ISBN según longitud y validez.
    Retorna: "ISBN-10", "ISBN-13" o "INVALID"
    """
    s_norm = normalize_isbn(s)
    if len(s_norm) == 10 and is_valid_isbn10(s_norm):
        return "ISBN-10"
    elif len(s_norm) == 13 and is_valid_isbn13(s_norm):
        return "ISBN-13"
    else:
        return "INVALID"
    

print(detect_isbn("0-306-40615-2"))  # → ISBN-10
print(detect_isbn("978-3-16-148410-0"))  # → ISBN-13
print(detect_isbn("123456789X"))  # → ISBN-10
print(detect_isbn("12345"))  # → INVALID