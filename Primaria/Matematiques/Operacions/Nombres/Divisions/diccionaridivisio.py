"""
Model de dades i lògica matemàtica per a l'aplicació de Divisions.
Gestiona la generació aleatòria de divisions per divisors d'1, 2 i 3 xifres
(amb residu i sense residu), construeix la seqüència pas a pas amb el mètode
de la caixa i prepara la comprovació (prova de la divisió).
"""
import random


def _construir_passos_divisio(dividend, divisor):
    """
    Construeix la llista ordenada de passos per explicar la divisió
    amb el mètode de la caixa i, al final, la prova de la divisió.
    """
    digits_div = [int(ch) for ch in str(dividend)]
    n_digits = len(digits_div)

    passos = []
    quocient_digits = []
    # Cada element de `files_calcul` representa una fila sota el dividend:
    # {"text": str, "col_fi": int (índex 0..n_digits-1 des de l'esquerra), "es_residu_final": bool}
    files_calcul = []

    idx = 0
    valor_actual = 0
    col_inici_grup = 0
    primer_grup = True

    while idx < n_digits:
        # Agafem xifres fins que el valor format sigui >= divisor, o bé fins arribar al final
        if primer_grup:
            col_inici_grup = idx
            valor_actual = digits_div[idx]
            while idx + 1 < n_digits and valor_actual < divisor:
                idx += 1
                valor_actual = valor_actual * 10 + digits_div[idx]
            primer_grup = False
        else:
            # Baixem una xifra nova del dividend
            valor_actual = valor_actual * 10 + digits_div[idx]

        xifra_q = valor_actual // divisor
        producte = xifra_q * divisor
        residu_pas = valor_actual - producte
        quocient_digits.append(xifra_q)

        # Afegim la fila del càlcul / residu parcial alineada amb la xifra actual (idx)
        files_calcul.append({
            "text": str(residu_pas),
            "col_fi": idx,
            "es_residu_final": False,
        })

        # Text explicatiu d'aquest pas
        if residu_pas == 0:
            exp = (
                f"Agafem {valor_actual}: busquem quin nombre multiplicat per {divisor} s'acosta més sense passar-se. "
                f"És {xifra_q} ({xifra_q} × {divisor} = {producte}). "
                f"Fem {valor_actual} − {producte} = 0 (divisió exacta en aquest pas)."
            )
        else:
            exp = (
                f"Agafem {valor_actual}: busquem quin nombre multiplicat per {divisor} s'acosta més sense passar-se. "
                f"És {xifra_q} ({xifra_q} × {divisor} = {producte}). "
                f"Fem {valor_actual} − {producte} = {residu_pas} de residu."
            )

        quocient_parcial = int("".join(str(d) for d in quocient_digits))

        passos.append({
            "tipus": "divisio_pas",
            "valor_actual": valor_actual,
            "divisor": divisor,
            "xifra_q": xifra_q,
            "producte": producte,
            "residu_pas": residu_pas,
            "col_inici": col_inici_grup,
            "col_fi": idx,
            "quocient_digits": list(quocient_digits),
            "quocient_parcial": quocient_parcial,
            "files_calcul": [dict(f) for f in files_calcul],
            "residu_final": None,
            "prova": None,
            "explicacio": exp,
        })

        valor_actual = residu_pas
        idx += 1

    quocient_final = int("".join(str(d) for d in quocient_digits)) if quocient_digits else 0
    residu_final = valor_actual

    if files_calcul:
        files_calcul[-1]["es_residu_final"] = True

    # Pas final: prova de la divisió -> Quocient * Divisor + Residu = Dividend
    producte_prova = quocient_final * divisor
    total_prova = producte_prova + residu_final

    if residu_final == 0:
        exp_prova = (
            f"Divisió acabada sense residu (residu = 0). "
            f"Prova de la divisió: Quocient ({quocient_final}) × Divisor ({divisor}) = {total_prova}, "
            f"que coincideix amb el dividend ({dividend})!"
        )
    else:
        exp_prova = (
            f"Divisió acabada amb residu {residu_final}. "
            f"Prova de la divisió: (Quocient {quocient_final} × Divisor {divisor}) + Residu ({residu_final}) "
            f"= {producte_prova} + {residu_final} = {total_prova}, que coincideix amb el dividend ({dividend})!"
        )

    passos.append({
        "tipus": "prova_divisio",
        "valor_actual": dividend,
        "divisor": divisor,
        "xifra_q": None,
        "producte": producte_prova,
        "residu_pas": residu_final,
        "col_inici": 0,
        "col_fi": n_digits - 1,
        "quocient_digits": list(quocient_digits),
        "quocient_parcial": quocient_final,
        "files_calcul": [dict(f) for f in files_calcul],
        "residu_final": residu_final,
        "prova": {
            "dividend": dividend,
            "divisor": divisor,
            "quocient": quocient_final,
            "residu": residu_final,
            "producte_prova": producte_prova,
            "total_prova": total_prova,
            "es_exacta": residu_final == 0,
        },
        "explicacio": exp_prova,
    })

    return {
        "dividend": dividend,
        "divisor": divisor,
        "quocient": quocient_final,
        "residu": residu_final,
        "es_exacta": residu_final == 0,
        "passos": passos,
    }


def generar_exercici_divisio(xifres_divisor, ultim_exercici=None):
    """
    Genera una divisió aleatòria amb residu o sense residu:
    - xifres_divisor = 1: dividend en [1..9999], divisor en [1..9]
    - xifres_divisor = 2: dividend en [1..9999], divisor yz amb y, z en [1..9]
    - xifres_divisor = 3: dividend en [1..9999], divisor yzm amb y, z, m en [1..9]
    """
    if xifres_divisor not in (1, 2, 3):
        raise ValueError("xifres_divisor ha de ser 1, 2 o 3.")

    for _ in range(400):
        if xifres_divisor == 1:
            divisor = random.randint(1, 9)
        elif xifres_divisor == 2:
            y = random.randint(1, 9)
            z = random.randint(1, 9)
            divisor = y * 10 + z
        else:
            y = random.randint(1, 9)
            z = random.randint(1, 9)
            m = random.randint(1, 9)
            divisor = y * 100 + z * 10 + m

        # Alternem de manera equilibrada divisions exactes (sense residu) i amb residu
        vol_exacta = random.choice([True, False])
        if vol_exacta:
            max_q = max(1, 9999 // divisor)
            q = random.randint(1, max_q)
            dividend = q * divisor
        else:
            dividend = random.randint(1, 9999)

        if ultim_exercici == (dividend, divisor):
            continue

        dades = _construir_passos_divisio(dividend, divisor)
        dades["xifres_divisor"] = xifres_divisor
        return dades

    divisor = 4 if xifres_divisor == 1 else (24 if xifres_divisor == 2 else 125)
    dividend = 975
    dades = _construir_passos_divisio(dividend, divisor)
    dades["xifres_divisor"] = xifres_divisor
    return dades