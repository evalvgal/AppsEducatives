"""
Model de dades i lògica matemàtica per a l'aplicació de Divisió de Fraccions.
Genera divisions de dues fraccions (a/b ÷ c/d) amb numeradors i denominadors
aleatoris en [1..30], i construeix els passos:
1) Numerador del resultat = numerador de la primera × denominador de la segona (a × d)
2) Denominador del resultat = denominador de la primera × numerador de la segona (b × c)
3+) Descomposició en factors primers (ratlla vertical), càlcul de l'M.C.D. i
   reducció de la fracció al màxim pas a pas.
"""
from collections import Counter
import math
import random


def _passos_descomposicio_vertical(n):
    """
    Construeix la llista acumulada d'etapes de la descomposició en factors primers
    (mètode de la ratlla vertical) per al nombre n (n >= 1).
    Cada etapa és una llista de diccionaris `{"nombre": ..., "divisor": ...}`.
    """
    if n <= 1:
        return [[{"nombre": n, "divisor": None}]]

    etapes = []
    files = []
    actual = n
    divisor = 2

    while actual > 1:
        while actual % divisor == 0:
            files.append({"nombre": actual, "divisor": divisor})
            actual //= divisor
            etapes.append([dict(f) for f in files] + [{"nombre": actual, "divisor": None}])
        divisor += 1

    return etapes


def _factors_primers_llista(n):
    """Retorna la llista ordenada de factors primers de n."""
    if n < 2:
        return []
    factors = []
    d = 2
    temp = n
    while d * d <= temp:
        while temp % d == 0:
            factors.append(d)
            temp //= d
        d += 1
    if temp > 1:
        factors.append(temp)
    return factors


def _calcular_mcd_per_factors(num, den):
    """
    Calcula l'M.C.D.(num, den) a partir de la descomposició en factors primers
    comuns amb menor exponent, i retorna el detall textual.
    """
    if num <= 0 or den <= 0:
        mcd_val = math.gcd(num, den)
        return mcd_val, [], f"M.C.D.({num}, {den}) = {mcd_val}."

    fa = _factors_primers_llista(num)
    fb = _factors_primers_llista(den)

    ca = Counter(fa)
    cb = Counter(fb)

    factors_comuns = []
    for p in sorted(set(ca.keys()) & set(cb.keys())):
        vegades = min(ca[p], cb[p])
        for _ in range(vegades):
            factors_comuns.append(p)

    mcd = math.gcd(num, den)

    str_fa = " × ".join(str(x) for x in fa) if fa else str(num)
    str_fb = " × ".join(str(x) for x in fb) if fb else str(den)

    if factors_comuns:
        str_comuns = " × ".join(str(x) for x in factors_comuns)
        explicacio = (
            f"Descomposem {num} = {str_fa} i {den} = {str_fb}. "
            f"Els factors primers comuns amb menor exponent són {str_comuns}, "
            f"per tant M.C.D.({num}, {den}) = {mcd}."
        )
    else:
        explicacio = (
            f"Descomposem {num} = {str_fa} i {den} = {str_fb}. "
            f"No tenen factors primers comuns (a part d'1), per tant M.C.D.({num}, {den}) = 1."
        )

    return mcd, factors_comuns, explicacio


def _passos_reduccio_detallats(num_inicial, den_inicial, base_estat):
    """
    Construeix els passos detallats de la reducció d'una fracció:
    1) Pas a pas de la descomposició en factors primers de `num_inicial` i `den_inicial`
    2) Conclusió del M.C.D.(num_inicial, den_inicial)
    3) Divisió pas a pas del numerador pel M.C.D.
    4) Divisió pas a pas del denominador pel M.C.D. i fracció final reduïda.
    """
    passos_red = []

    etapes_num = _passos_descomposicio_vertical(num_inicial)
    etapes_den = _passos_descomposicio_vertical(den_inicial)
    mcd, factors_comuns, exp_mcd = _calcular_mcd_per_factors(num_inicial, den_inicial)

    num_reduit = num_inicial // mcd
    den_reduit = den_inicial // mcd

    n_etapes_desc = max(len(etapes_num), len(etapes_den))

    for i in range(n_etapes_desc):
        desc_n = etapes_num[min(i, len(etapes_num) - 1)]
        desc_d = etapes_den[min(i, len(etapes_den) - 1)]

        ultim_n = desc_n[-1]
        ultim_d = desc_d[-1]

        parts_exp = []
        if i < len(etapes_num) and len(desc_n) >= 2 and desc_n[-2]["divisor"] is not None:
            ant_n = desc_n[-2]["nombre"]
            div_n = desc_n[-2]["divisor"]
            parts_exp.append(f"En {num_inicial}: {ant_n} ÷ {div_n} = {ultim_n}")
        elif i >= len(etapes_num):
            parts_exp.append(f"La descomposició de {num_inicial} ja és completa")

        if i < len(etapes_den) and len(desc_d) >= 2 and desc_d[-2]["divisor"] is not None:
            ant_d = desc_d[-2]["nombre"]
            div_d = desc_d[-2]["divisor"]
            parts_exp.append(f"En {den_inicial}: {ant_d} ÷ {div_d} = {ultim_d}")
        elif i >= len(etapes_den):
            parts_exp.append(f"La descomposició de {den_inicial} ja és completa")

        estat = dict(base_estat)
        estat.update({
            "fase": "reduccio_descomposicio",
            "num_a_reduir": num_inicial,
            "den_a_reduir": den_inicial,
            "desc_num_files": desc_n,
            "desc_den_files": desc_d,
            "mcd": None,
            "factors_comuns_mcd": factors_comuns,
            "div_num_fet": False,
            "div_den_fet": False,
            "num_reduit": None,
            "den_reduit": None,
            "titol_pas": f"Reducció de {num_inicial}/{den_inicial}: descomposició en factors primers",
            "explicacio": (
                f"Reducció de {num_inicial}/{den_inicial} (pas {i + 1} de {n_etapes_desc}): "
                + (". ".join(parts_exp) + "." if parts_exp else f"Iniciem la descomposició de {num_inicial} i {den_inicial}.")
            ),
        })
        passos_red.append(estat)

    estat_mcd = dict(base_estat)
    estat_mcd.update({
        "fase": "reduccio_mcd",
        "num_a_reduir": num_inicial,
        "den_a_reduir": den_inicial,
        "desc_num_files": etapes_num[-1],
        "desc_den_files": etapes_den[-1],
        "mcd": mcd,
        "factors_comuns_mcd": factors_comuns,
        "div_num_fet": False,
        "div_den_fet": False,
        "num_reduit": None,
        "den_reduit": None,
        "titol_pas": f"Reducció de {num_inicial}/{den_inicial}: conclusió del M.C.D.",
        "explicacio": f"Reducció de {num_inicial}/{den_inicial}: {exp_mcd}",
    })
    passos_red.append(estat_mcd)

    estat_div_num = dict(base_estat)
    estat_div_num.update({
        "fase": "reduccio_div_num",
        "num_a_reduir": num_inicial,
        "den_a_reduir": den_inicial,
        "desc_num_files": etapes_num[-1],
        "desc_den_files": etapes_den[-1],
        "mcd": mcd,
        "factors_comuns_mcd": factors_comuns,
        "div_num_fet": True,
        "div_den_fet": False,
        "num_reduit": num_reduit,
        "den_reduit": None,
        "titol_pas": f"Reducció de {num_inicial}/{den_inicial}: dividim el numerador entre {mcd}",
        "explicacio": (
            f"Reducció de {num_inicial}/{den_inicial}: dividim el numerador ({num_inicial}) "
            f"entre el M.C.D. ({mcd}): {num_inicial} ÷ {mcd} = {num_reduit}."
        ),
    })
    passos_red.append(estat_div_num)

    if mcd > 1:
        exp_final = (
            f"Reducció de {num_inicial}/{den_inicial}: dividim el denominador ({den_inicial}) "
            f"entre el M.C.D. ({mcd}): {den_inicial} ÷ {mcd} = {den_reduit}. "
            f"La fracció reduïda al màxim és {num_reduit}/{den_reduit}."
        )
    else:
        exp_final = (
            f"Reducció de {num_inicial}/{den_inicial}: dividim el denominador ({den_inicial}) "
            f"entre el M.C.D. (1): {den_inicial} ÷ 1 = {den_reduit}. "
            f"Com que el M.C.D. és 1, la fracció ja és irreductible: {num_reduit}/{den_reduit}."
        )

    estat_div_den = dict(base_estat)
    estat_div_den.update({
        "fase": "reduccio_final",
        "num_a_reduir": num_inicial,
        "den_a_reduir": den_inicial,
        "desc_num_files": etapes_num[-1],
        "desc_den_files": etapes_den[-1],
        "mcd": mcd,
        "factors_comuns_mcd": factors_comuns,
        "div_num_fet": True,
        "div_den_fet": True,
        "num_reduit": num_reduit,
        "den_reduit": den_reduit,
        "titol_pas": f"Reducció de {num_inicial}/{den_inicial}: dividim el denominador entre {mcd}",
        "explicacio": exp_final,
    })
    passos_red.append(estat_div_den)

    return passos_red, num_reduit, den_reduit


def _construir_exercici_divisio(a, b, c, d):
    """
    Construeix tots els passos d'una divisió de dues fraccions (a/b ÷ c/d)
    aplicant directament la regla:
    - numerador del resultat = a * d (numerador de la 1a × denominador de la 2a)
    - denominador del resultat = b * c (denominador de la 1a × numerador de la 2a)
    i tot seguit la reducció amb M.C.D.
    """
    num_resultat = a * d
    den_resultat = b * c

    estat_base = {
        "a": a,
        "b": b,
        "c": c,
        "d": d,
        "num_calc_fet": False,
        "den_calc_fet": False,
        "num_resultat": None,
        "den_resultat": None,
        "num_a_reduir": None,
        "den_a_reduir": None,
        "desc_num_files": [],
        "desc_den_files": [],
        "mcd": None,
        "factors_comuns_mcd": [],
        "div_num_fet": False,
        "div_den_fet": False,
        "num_reduit": None,
        "den_reduit": None,
    }

    passos = []

    p1 = dict(estat_base)
    p1.update({
        "fase": "calc_numerador",
        "num_calc_fet": True,
        "titol_pas": "1. Calculem el numerador del resultat",
        "explicacio": (
            f"Per dividir {a}/{b} ÷ {c}/{d}, el numerador del resultat és el producte del "
            f"numerador de la primera fracció ({a}) pel denominador de la segona ({d}): "
            f"{a} × {d} = {num_resultat}."
        ),
    })
    passos.append(p1)

    p2 = dict(p1)
    p2.update({
        "fase": "calc_denominador",
        "den_calc_fet": True,
        "num_resultat": num_resultat,
        "den_resultat": den_resultat,
        "titol_pas": "2. Calculem el denominador del resultat",
        "explicacio": (
            f"El denominador del resultat és el producte del denominador de la primera fracció "
            f"({b}) pel numerador de la segona ({c}): {b} × {c} = {den_resultat}. "
            f"Així obtenim la fracció resultat {num_resultat}/{den_resultat}."
        ),
    })
    passos.append(p2)

    passos_red, num_red, den_red = _passos_reduccio_detallats(num_resultat, den_resultat, p2)
    passos.extend(passos_red)

    return {
        "a": a,
        "b": b,
        "c": c,
        "d": d,
        "num_resultat": num_resultat,
        "den_resultat": den_resultat,
        "num_reduit": num_red,
        "den_reduit": den_red,
        "passos": passos,
    }


def generar_exercici_divisio(ultim_exercici=None):
    """
    Genera aleatòriament una divisió de dues fraccions (a/b ÷ c/d)
    on tant els numeradors com els denominadors estan en l'interval [1..30].
    """
    for _ in range(200):
        a = random.randint(1, 30)
        b = random.randint(1, 30)
        c = random.randint(1, 30)
        d = random.randint(1, 30)

        clau = (a, b, c, d)
        if ultim_exercici == clau:
            continue

        exercici = _construir_exercici_divisio(a, b, c, d)
        exercici["clau"] = clau
        return exercici

    a, b, c, d = 6, 8, 3, 4
    exercici = _construir_exercici_divisio(a, b, c, d)
    exercici["clau"] = (a, b, c, d)
    return exercici