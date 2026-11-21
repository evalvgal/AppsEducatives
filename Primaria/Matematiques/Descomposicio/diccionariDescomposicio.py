"""
Model de dades i lògica matemàtica per a l'aplicació de Descomposició Factorial.
Conté el càlcul de nombres primers fins al 1000, les definicions teòriques,
l'exemple resolt per a la teoria i el generador d'exercicis aleatoris pas a pas.
"""
import random


def obtenir_primers_fins(limit=1000):
    """Retorna la llista de nombres primers entre 1 i `limit` (Garbell d'Eratòstenes)."""
    if limit < 2:
        return []
    es_primer = [True] * (limit + 1)
    es_primer[0] = False
    es_primer[1] = False

    p = 2
    while p * p <= limit:
        if es_primer[p]:
            for multiple in range(p * p, limit + 1, p):
                es_primer[multiple] = False
        p += 1

    return [num for num, primer in enumerate(es_primer) if primer]


def calcular_passos_descomposicio(nombre):
    """
    Calcula la descomposició pas a pas d'un nombre en factors primers.
    Retorna una llista de tuples: (dividend_actual, divisor_primer, nou_quocient)
    """
    passos = []
    actual = nombre
    divisor = 2

    while actual > 1:
        while actual % divisor == 0:
            nou = actual // divisor
            passos.append((actual, divisor, nou))
            actual = nou
        divisor += 1
        if divisor * divisor > actual and actual > 1:
            passos.append((actual, actual, 1))
            actual = 1

    return passos


def obtenir_termes_potencies(passos):
    """
    Retorna una llista de tuples (base_str, exponent_str_o_None) a partir dels passos.
    Exemple per a 96: [('2', '5'), ('3', None)]
    """
    if not passos:
        return []

    exponents = {}
    ordre_factors = []
    for _, factor, _ in passos:
        if factor not in exponents:
            exponents[factor] = 0
            ordre_factors.append(factor)
        exponents[factor] += 1

    termes = []
    for f in ordre_factors:
        exp = exponents[f]
        termes.append((str(f), str(exp) if exp > 1 else None))

    return termes


def formatar_expressio_potencies(passos):
    """Retorna una representació en text llegible del tipus: 2(5) · 3."""
    termes = obtenir_termes_potencies(passos)
    if not termes:
        return ""
    parts = [f"{base}({exp})" if exp else base for base, exp in termes]
    return " · ".join(parts)


PRIMERS_1_1000 = obtenir_primers_fins(1000)

TEORIA_PAGINA_1 = {
    "titol": "Nombres primers",
    "definicio": (
        "Un nombre primer és un nombre natural més gran que 1 que només té dos divisors "
        "positius diferents: ell mateix i el nombre 1. Si té més divisors, s'anomena nombre compost. "
        "El nombre 1 no es considera ni primer ni compost."
    ),
    "subtitol_llista": "Nombres primers del 1 al 1000:",
    "primers": PRIMERS_1_1000,
}

EXEMPLE_TEORIA_NUMERO = 360
_PASSOS_EXEMPLE = calcular_passos_descomposicio(EXEMPLE_TEORIA_NUMERO)

TEORIA_PAGINA_2 = {
    "titol": "Descomposició factorial",
    "definicio": (
        "Descompondre un nombre en factors primers (o descomposició factorial) consisteix a "
        "expressar-lo com un producte de nombres primers. Per fer-ho, escrivim el nombre a "
        "l'esquerra d'una ratlla vertical i anem dividint successivament per nombres primers "
        "(2, 3, 5, 7, 11...) fins arribar a 1 a la columna esquerra."
    ),
    "exemple_numero": EXEMPLE_TEORIA_NUMERO,
    "exemple_passos": _PASSOS_EXEMPLE,
    "exemple_producte": " · ".join(str(p[1]) for p in _PASSOS_EXEMPLE),
    "exemple_potencies": formatar_expressio_potencies(_PASSOS_EXEMPLE),
    "exemple_termes": obtenir_termes_potencies(_PASSOS_EXEMPLE),
}

# Nombres recomanats per a primària (variats: parells, múltiples de 3 i 5, i algun amb factor primer més alt)
NOMBRES_EXERCICIS = [
    24, 36, 40, 45, 48, 50, 54, 60, 63, 70,
    72, 75, 80, 84, 90, 96, 98, 100, 105, 108,
    112, 120, 126, 132, 140, 144, 150, 160, 168, 180,
    196, 200, 210, 225, 240, 250, 270, 300, 315, 360,
]


def generar_exercici_aleatori(ultim_nombre=None):
    """Tria un nombre aleatori diferent de l'anterior i en prepara els passos."""
    opcions = [n for n in NOMBRES_EXERCICIS if n != ultim_nombre] or NOMBRES_EXERCICIS
    nombre = random.choice(opcions)
    passos = calcular_passos_descomposicio(nombre)
    return {
        "nombre": nombre,
        "passos": passos,
        "producte": " · ".join(str(p[1]) for p in passos),
        "potencies": formatar_expressio_potencies(passos),
        "termes_potencies": obtenir_termes_potencies(passos),
    }