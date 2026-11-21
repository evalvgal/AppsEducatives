"""
Model de dades i lògica matemàtica per a l'aplicació de Mínim Comú Múltiple (m.c.m.)
i Màxim Comú Divisor (M.C.D.).
Conté el càlcul pas a pas de descomposició factorial amb ratlla vertical, l'obtenció
dels factors comuns i no comuns amb potències, les definicions de teoria i el
generador de parelles de nombres aleatoris per als exercicis resolts.
"""
import math
import random


SUPERINDEXS = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
}


def formatar_potencia(base, exponent):
    """Formata una base i exponent com '2³' (si exponent == 1, retorna '2')."""
    if exponent == 1:
        return str(base)
    exp_str = "".join(SUPERINDEXS.get(ch, f"^{ch}") for ch in str(exponent))
    return f"{base}{exp_str}"


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


def obtenir_diccionari_factors(passos):
    """Retorna un diccionari {factor_primer: exponent} a partir dels passos."""
    factors = {}
    for _, factor, _ in passos:
        factors[factor] = factors.get(factor, 0) + 1
    return factors


def formatar_producte_potencies(factors_dict):
    """Converteix {2: 3, 3: 1} en '2³ · 3' ordenat per factor primer."""
    if not factors_dict:
        return "1"
    parts = [formatar_potencia(base, factors_dict[base]) for base in sorted(factors_dict.keys())]
    return " · ".join(parts)


def analitzar_parella(x, y):
    """
    Analitza dos nombres x i y per obtenir:
    - Els passos de descomposició de x i de y
    - L'expressió en factors primers de x i de y
    - El detall dels factors escollits per al m.c.m. (comuns i no comuns amb major exponent)
    - El detall dels factors escollits per al M.C.D. (comuns amb menor exponent)
    - Els valors finals de m.c.m.(x, y) i M.C.D.(x, y)
    """
    passos_x = calcular_passos_descomposicio(x)
    passos_y = calcular_passos_descomposicio(y)

    factors_x = obtenir_diccionari_factors(passos_x)
    factors_y = obtenir_diccionari_factors(passos_y)

    tots_factors = sorted(set(factors_x.keys()) | set(factors_y.keys()))
    comuns = sorted(set(factors_x.keys()) & set(factors_y.keys()))

    # Càlcul del m.c.m.: comuns i no comuns amb el major exponent
    factors_mcm = {}
    for f in tots_factors:
        factors_mcm[f] = max(factors_x.get(f, 0), factors_y.get(f, 0))

    valor_mcm = math.lcm(x, y)
    expressio_mcm = formatar_producte_potencies(factors_mcm)

    # Càlcul del M.C.D.: només comuns amb el menor exponent
    factors_mcd = {}
    for f in comuns:
        factors_mcd[f] = min(factors_x[f], factors_y[f])

    valor_mcd = math.gcd(x, y)
    expressio_mcd = formatar_producte_potencies(factors_mcd) if factors_mcd else "1 (no tenen factors primers comuns)"

    return {
        "x": x,
        "y": y,
        "passos_x": passos_x,
        "passos_y": passos_y,
        "factors_x_str": formatar_producte_potencies(factors_x),
        "factors_y_str": formatar_producte_potencies(factors_y),
        "mcm_valor": valor_mcm,
        "mcm_expressio": expressio_mcm,
        "mcd_valor": valor_mcd,
        "mcd_expressio": expressio_mcd,
        "te_comuns": len(comuns) > 0,
    }


# Dades de Teoria - Pàgina 1: Mínim Comú Múltiple
EXEMPLE_MCM_DADES = analitzar_parella(12, 18)

TEORIA_PAGINA_1 = {
    "titol": "Mínim Comú Múltiple (m.c.m.)",
    "definicio": (
        "El mínim comú múltiple (m.c.m.) de dos o més nombres naturals és el múltiple "
        "comú més petit diferent de zero. Per calcular-lo: 1) Descomposem cada nombre "
        "en factors primers amb la ratlla vertical. 2) Multipliquem els factors primers "
        "comuns i no comuns elevats al seu major exponent."
    ),
    "exemple": EXEMPLE_MCM_DADES,
}

# Dades de Teoria - Pàgina 2: Màxim Comú Divisor
EXEMPLE_MCD_DADES = analitzar_parella(24, 36)

TEORIA_PAGINA_2 = {
    "titol": "Màxim Comú Divisor (M.C.D.)",
    "definicio": (
        "El màxim comú divisor (M.C.D.) de dos o més nombres naturals és el divisor comú "
        "més gran que els divideix de manera exacta. Per calcular-lo: 1) Descomposem cada "
        "nombre en factors primers amb la ratlla vertical. 2) Multipliquem només els "
        "factors primers comuns elevats al seu menor exponent."
    ),
    "exemple": EXEMPLE_MCD_DADES,
}

# Parella de nombres adients per a Educació Primària
PARELLES_EXERCICIS = [
    (12, 18), (15, 20), (16, 24), (18, 24), (20, 30),
    (24, 36), (28, 42), (30, 45), (32, 48), (36, 48),
    (40, 60), (45, 75), (48, 72), (50, 75), (54, 72),
    (60, 84), (60, 90), (72, 96), (80, 120), (90, 150),
    (14, 21), (25, 35), (18, 30), (24, 40), (36, 54),
]


def generar_exercici_aleatori(ultima_parella=None):
    """Selecciona una parella aleatòria diferent de l'anterior i en prepara la resolució."""
    opcions = [p for p in PARELLES_EXERCICIS if p != ultima_parella] or PARELLES_EXERCICIS
    x, y = random.choice(opcions)
    if random.choice([True, False]):
        x, y = y, x
    return analitzar_parella(x, y)