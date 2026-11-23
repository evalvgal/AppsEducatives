"""
Model de dades i lògica matemàtica per a l'aplicació de Resta de Fraccions.
Genera restes de dues fraccions on la segona fracció és sempre menor que la
primera (mateix denominador en [1..999]; diferents denominadors en [1..50]),
construeix els passos del càlcul de l'm.c.m. (amb descomposició en ratlla
vertical pas a pas), els passos de la resta, la descomposició factorial pas a
pas del numerador i del denominador del resultat per trobar-ne l'M.C.D., i les
divisions per reduir la fracció al màxim.
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


def _calcular_mcm_per_factors(b, d):
    """
    Calcula l'm.c.m.(b, d) a partir dels factors primers comuns i no comuns
    amb major exponent, i retorna el detall textual.
    """
    fb = _factors_primers_llista(b)
    fd = _factors_primers_llista(d)

    cb = Counter(fb)
    cd = Counter(fd)

    tots_primers = sorted(set(cb.keys()) | set(cd.keys()))
    factors_mcm = []
    for p in tots_primers:
        vegades = max(cb[p], cd[p])
        for _ in range(vegades):
            factors_mcm.append(p)

    mcm = math.lcm(b, d)

    str_fb = " × ".join(str(x) for x in fb) if fb else str(b)
    str_fd = " × ".join(str(x) for x in fd) if fd else str(d)

    if factors_mcm:
        str_mcm = " × ".join(str(x) for x in factors_mcm)
        explicacio = (
            f"Descomposem {b} = {str_fb} i {d} = {str_fd}. "
            f"Agafem els factors primers comuns i no comuns amb major exponent: "
            f"{str_mcm} = {mcm}. Per tant, m.c.m.({b}, {d}) = {mcm}."
        )
    else:
        explicacio = f"m.c.m.({b}, {d}) = {mcm}."

    return mcm, factors_mcm, explicacio


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


def _construir_exercici_mateix_denominador(a, b, den):
    """
    Construeix tots els passos d'una resta a/den - b/den (amb a > b)
    i la seva reducció amb M.C.D.
    """
    num_resultat = a - b
    den_resultat = den

    estat_base = {
        "mateix_denominador": True,
        "a": a,
        "b": b,
        "den": den,
        "c": None,
        "d": None,
        "mcm": den,
        "mcm_complet": True,
        "desc_b_files": [],
        "desc_d_files": [],
        "factor_a": 1,
        "factor_c": 1,
        "a_eq": a,
        "c_eq": b,
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
        "fase": "inici",
        "titol_pas": "1. Mateix denominador",
        "explicacio": (
            f"Volem restar {a}/{den} - {b}/{den} (la segona fracció és menor que la primera, "
            f"ja que {b}/{den} < {a}/{den}). Com que tenen el mateix denominador ({den}), "
            f"conservem {den} i restem els numeradors ({a} - {b})."
        ),
    })
    passos.append(p1)

    p2 = dict(estat_base)
    p2.update({
        "fase": "resta_directa",
        "num_resultat": num_resultat,
        "den_resultat": den_resultat,
        "titol_pas": "2. Restem els numeradors",
        "explicacio": (
            f"Restem els numeradors: {a} - {b} = {num_resultat}, i mantenim el denominador comú {den_resultat}. "
            f"Obtenim la fracció resultat {num_resultat}/{den_resultat}."
        ),
    })
    passos.append(p2)

    passos_red, num_red, den_red = _passos_reduccio_detallats(num_resultat, den_resultat, p2)
    passos.extend(passos_red)

    return {
        "mateix_denominador": True,
        "a": a,
        "b": b,
        "den": den,
        "c": None,
        "d": None,
        "mcm": den,
        "num_resultat": num_resultat,
        "den_resultat": den_resultat,
        "num_reduit": num_red,
        "den_reduit": den_red,
        "passos": passos,
    }


def _construir_exercici_diferent_denominador(a, b, c, d):
    """
    Construeix tots els passos d'una resta a/b - c/d (amb a/b > c/d)
    amb denominadors diferents:
    - Descomposició pas a pas de b i d per trobar l'm.c.m.
    - Conclusió de l'm.c.m.
    - Fraccions equivalents a denominador m.c.m.
    - Resta de numeradors
    - Reducció amb M.C.D.
    """
    etapes_b = _passos_descomposicio_vertical(b)
    etapes_d = _passos_descomposicio_vertical(d)
    mcm, _, exp_mcm = _calcular_mcm_per_factors(b, d)

    factor_a = mcm // b
    factor_c = mcm // d
    a_eq = a * factor_a
    c_eq = c * factor_c
    num_resultat = a_eq - c_eq
    den_resultat = mcm

    estat_base = {
        "mateix_denominador": False,
        "a": a,
        "b": b,
        "c": c,
        "d": d,
        "den": None,
        "mcm": None,
        "mcm_complet": False,
        "desc_b_files": [],
        "desc_d_files": [],
        "factor_a": None,
        "factor_c": None,
        "a_eq": None,
        "c_eq": None,
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

    n_etapes_mcm = max(len(etapes_b), len(etapes_d))
    for i in range(n_etapes_mcm):
        fb_act = etapes_b[min(i, len(etapes_b) - 1)]
        fd_act = etapes_d[min(i, len(etapes_d) - 1)]

        parts_exp = []
        if i < len(etapes_b) and len(fb_act) >= 2 and fb_act[-2]["divisor"] is not None:
            parts_exp.append(f"En {b}: {fb_act[-2]['nombre']} ÷ {fb_act[-2]['divisor']} = {fb_act[-1]['nombre']}")
        elif i >= len(etapes_b):
            parts_exp.append(f"La descomposició de {b} ja és completa")

        if i < len(etapes_d) and len(fd_act) >= 2 and fd_act[-2]["divisor"] is not None:
            parts_exp.append(f"En {d}: {fd_act[-2]['nombre']} ÷ {fd_act[-2]['divisor']} = {fd_act[-1]['nombre']}")
        elif i >= len(etapes_d):
            parts_exp.append(f"La descomposició de {d} ja és completa")

        p_desc = dict(estat_base)
        p_desc.update({
            "fase": "mcm_descomposicio",
            "mcm_complet": False,
            "desc_b_files": fb_act,
            "desc_d_files": fd_act,
            "titol_pas": f"1. Càlcul de l'm.c.m.({b}, {d}): descomposició en factors primers",
            "explicacio": (
                f"Per restar {a}/{b} - {c}/{d} (on {c}/{d} < {a}/{b}), calculem l'm.c.m.({b}, {d}) "
                f"(pas {i + 1} de {n_etapes_mcm}): "
                + (". ".join(parts_exp) + "." if parts_exp else f"Descomposem {b} i {d}.")
            ),
        })
        passos.append(p_desc)

    p1 = dict(estat_base)
    p1.update({
        "fase": "mcm",
        "mcm": mcm,
        "mcm_complet": True,
        "desc_b_files": etapes_b[-1],
        "desc_d_files": etapes_d[-1],
        "titol_pas": f"1. Conclusió del denominador comú: m.c.m.({b}, {d}) = {mcm}",
        "explicacio": exp_mcm,
    })
    passos.append(p1)

    p2 = dict(p1)
    p2.update({
        "fase": "eq_primera",
        "factor_a": factor_a,
        "a_eq": a_eq,
        "titol_pas": f"2. Passem {a}/{b} a denominador {mcm}",
        "explicacio": (
            f"Dividim el nou denominador ({mcm}) entre el denominador de la primera fracció ({b}): "
            f"{mcm} ÷ {b} = {factor_a}. Multipliquem el numerador pel mateix factor: "
            f"{a} × {factor_a} = {a_eq}. Així, {a}/{b} = {a_eq}/{mcm}."
        ),
    })
    passos.append(p2)

    p3 = dict(p2)
    p3.update({
        "fase": "eq_segona",
        "factor_c": factor_c,
        "c_eq": c_eq,
        "titol_pas": f"3. Passem {c}/{d} a denominador {mcm}",
        "explicacio": (
            f"Dividim el nou denominador ({mcm}) entre el denominador de la segona fracció ({d}): "
            f"{mcm} ÷ {d} = {factor_c}. Multipliquem el numerador pel mateix factor: "
            f"{c} × {factor_c} = {c_eq}. Així, {c}/{d} = {c_eq}/{mcm}."
        ),
    })
    passos.append(p3)

    p4 = dict(p3)
    p4.update({
        "fase": "resta_equivalents",
        "num_resultat": num_resultat,
        "den_resultat": den_resultat,
        "titol_pas": "4. Restem les fraccions equivalents",
        "explicacio": (
            f"Ara que tenen el mateix denominador ({mcm}), restem els numeradors: "
            f"{a_eq} - {c_eq} = {num_resultat} i conservem el denominador {den_resultat}. "
            f"El resultat de la resta és {num_resultat}/{den_resultat}."
        ),
    })
    passos.append(p4)

    passos_red, num_red, den_red = _passos_reduccio_detallats(num_resultat, den_resultat, p4)
    passos.extend(passos_red)

    return {
        "mateix_denominador": False,
        "a": a,
        "b": b,
        "c": c,
        "d": d,
        "den": None,
        "mcm": mcm,
        "num_resultat": num_resultat,
        "den_resultat": den_resultat,
        "num_reduit": num_red,
        "den_reduit": den_red,
        "passos": passos,
    }


def generar_exercici_resta(mateix_denominador, ultim_exercici=None):
    """
    Genera aleatòriament una resta de dues fraccions on la segona fracció
    sempre és estrictament menor que la primera:
    - mateix_denominador = True: a/den - b/den amb a, b, den en [1..999] i a > b.
    - mateix_denominador = False: a/b - c/d amb a, b, c, d en [1..50], b != d i a/b > c/d.
    """
    for _ in range(500):
        afavorir_reduible = random.random() < 0.75

        if mateix_denominador:
            if afavorir_reduible:
                factor = random.randint(2, 18)
                max_den = max(1, 999 // factor)
                den = random.randint(1, max_den)
                max_a = max(2, 999 // factor)
                a = random.randint(2, max_a) * factor
                max_b = max(1, (a - 1) // factor)
                b = random.randint(1, max_b) * factor
                a = min(999, a)
                b = min(999, b)
            else:
                den = random.randint(1, 999)
                a = random.randint(2, 999)
                b = random.randint(1, a - 1)

            if not (a > b and 1 <= a <= 999 and 1 <= b <= 999 and 1 <= den <= 999):
                continue

            clau = ("mateix", a, b, den)
            if ultim_exercici == clau:
                continue
            exercici = _construir_exercici_mateix_denominador(a, b, den)
            exercici["clau"] = clau
            return exercici
        else:
            b = random.randint(1, 50)
            d = random.randint(1, 50)
            if b == d:
                continue

            # Busquem a i c en [1..50] tals que a/b > c/d  <=>  a * d > c * b
            a = random.randint(1, 50)
            max_c_possible = (a * d - 1) // b
            if max_c_possible < 1:
                continue
            c = random.randint(1, min(50, max_c_possible))

            # En una part de casos, procurem que a_eq - c_eq sigui múltiple d'un factor comú amb mcm
            if afavorir_reduible and random.random() < 0.5:
                mcm = math.lcm(b, d)
                divisor_comu = random.randint(2, 6)
                if mcm % divisor_comu == 0:
                    # Ajustem a o c si cal mantenint a/b > c/d en [1..50]
                    pass

            if not (a * d > c * b):
                continue

            clau = ("diferent", a, b, c, d)
            if ultim_exercici == clau:
                continue
            exercici = _construir_exercici_diferent_denominador(a, b, c, d)
            exercici["clau"] = clau
            return exercici

    if mateix_denominador:
        exercici = _construir_exercici_mateix_denominador(10, 4, 18)
        exercici["clau"] = ("mateix", 10, 4, 18)
        return exercici
    exercici = _construir_exercici_diferent_denominador(5, 6, 1, 4)
    exercici["clau"] = ("diferent", 5, 6, 1, 4)
    return exercici