"""
Model de dades i lògica matemàtica per a l'aplicació de Divisions.
Gestiona la generació aleatòria de divisions per divisors d'1, 2 i 3 xifres
(amb residu i sense residu), construeix la seqüència pas a pas amb el mètode
de la caixa (incloent-hi el pas intermedi de baixar cada xifra del dividend)
i construeix la prova de la divisió pas a pas: multiplicació amb portades,
suma columna a columna dels productes parcials i suma del residu.
"""
import random


def _descompondre_xifres_dreta_a_esquerra(nombre):
    """Retorna les xifres d'un nombre de dreta a esquerra (unitats, desenes, centenes...)."""
    return [int(ch) for ch in reversed(str(nombre))]


def _construir_passos_prova_divisio(dividend, divisor, quocient, residu, files_calcul_previes, quocient_digits):
    """
    Construeix els passos detallats de la prova de la divisió:
    1) Multiplicació pas a pas de quocient * divisor (xifra a xifra del divisor, de dreta a esquerra)
    2) Si hi ha més d'una fila de productes parcials, suma columna per columna amb portades
    3) Suma del residu pas a pas i comprovació final amb el dividend.
    """
    passos_prova = []

    xifres_q = _descompondre_xifres_dreta_a_esquerra(quocient)
    xifres_d = _descompondre_xifres_dreta_a_esquerra(divisor)
    n_files_mult = len(xifres_d)

    files_parcials = [[] for _ in range(n_files_mult)]
    portades_sortida = [[0] * len(xifres_q) for _ in range(n_files_mult)]

    noms_posicio = [
        "unitats", "desenes", "centenes", "unitats de miler",
        "desenes de miler", "centenes de miler", "unitats de milió"
    ]
    noms_divisor = ["unitats", "desenes", "centenes"]

    # 1. Passos de multiplicació: quocient * divisor
    for idx_fila, dd in enumerate(xifres_d):
        portada_entrant = 0
        nom_d = noms_divisor[idx_fila] if idx_fila < len(noms_divisor) else f"posició {idx_fila + 1}"

        for pos_q, dq in enumerate(xifres_q):
            nom_q = noms_posicio[pos_q] if pos_q < len(noms_posicio) else f"posició {pos_q + 1}"
            producte_base = dq * dd
            total = producte_base + portada_entrant
            xifra_res = total % 10
            portada_nova = total // 10

            files_parcials[idx_fila].append(xifra_res)
            portades_sortida[idx_fila][pos_q] = portada_nova

            if portada_entrant > 0:
                exp = (
                    f"Prova — multiplicació ({nom_d}, multiplicant per {dd}): "
                    f"fem {dq} ({nom_q}) × {dd} = {producte_base}, hi sumem la portada {portada_entrant} → {total}. "
                    f"Posem {xifra_res}" + (f" i ens emportem {portada_nova}." if portada_nova > 0 else ".")
                )
            else:
                exp = (
                    f"Prova — multiplicació ({nom_d}, multiplicant per {dd}): "
                    f"fem {dq} ({nom_q}) × {dd} = {producte_base}. "
                    f"Posem {xifra_res}" + (f" i ens emportem {portada_nova}." if portada_nova > 0 else ".")
                )

            passos_prova.append({
                "tipus": "prova_mult_pas",
                "valor_actual": quocient,
                "divisor": divisor,
                "xifra_baixada": None,
                "xifra_q": dq,
                "dd": dd,
                "idx_fila": idx_fila,
                "pos_q": pos_q,
                "col_suma": None,
                "producte_base": producte_base,
                "portada_entrant": portada_entrant,
                "total": total,
                "xifra_res": xifra_res,
                "portada_nova": portada_nova,
                "producte": None,
                "residu_pas": residu,
                "col_inici": 0,
                "col_fi": len(str(dividend)) - 1,
                "col_baixada": None,
                "quocient_digits": list(quocient_digits),
                "quocient_parcial": quocient,
                "files_calcul": [dict(f) for f in files_calcul_previes],
                "residu_final": residu,
                "prova": {
                    "fase": "multiplicant",
                    "dividend": dividend,
                    "divisor": divisor,
                    "quocient": quocient,
                    "residu": residu,
                    "files_parcials": [list(f) for f in files_parcials],
                    "portades_sortida": [list(p) for p in portades_sortida],
                    "digits_suma_parcials": [],
                    "portades_suma_parcials": [],
                    "producte_quocient_divisor": None,
                    "digits_suma_residu": [],
                    "portades_suma_residu": [],
                    "total_amb_residu": None,
                    "es_exacta": residu == 0,
                },
                "explicacio": exp,
            })

            portada_entrant = portada_nova

        if portada_entrant > 0:
            files_parcials[idx_fila].append(portada_entrant)
            exp_baixa = (
                f"Prova — multiplicació ({nom_d}): no queden més xifres al quocient ({quocient}), "
                f"baixem la portada {portada_entrant}."
            )
            passos_prova.append({
                "tipus": "prova_mult_pas",
                "valor_actual": quocient,
                "divisor": divisor,
                "xifra_baixada": None,
                "xifra_q": None,
                "dd": dd,
                "idx_fila": idx_fila,
                "pos_q": len(xifres_q),
                "col_suma": None,
                "producte_base": None,
                "portada_entrant": portada_entrant,
                "total": portada_entrant,
                "xifra_res": portada_entrant,
                "portada_nova": 0,
                "producte": None,
                "residu_pas": residu,
                "col_inici": 0,
                "col_fi": len(str(dividend)) - 1,
                "col_baixada": None,
                "quocient_digits": list(quocient_digits),
                "quocient_parcial": quocient,
                "files_calcul": [dict(f) for f in files_calcul_previes],
                "residu_final": residu,
                "prova": {
                    "fase": "multiplicant",
                    "dividend": dividend,
                    "divisor": divisor,
                    "quocient": quocient,
                    "residu": residu,
                    "files_parcials": [list(f) for f in files_parcials],
                    "portades_sortida": [list(p) for p in portades_sortida],
                    "digits_suma_parcials": [],
                    "portades_suma_parcials": [],
                    "producte_quocient_divisor": None,
                    "digits_suma_residu": [],
                    "portades_suma_residu": [],
                    "total_amb_residu": None,
                    "es_exacta": residu == 0,
                },
                "explicacio": exp_baixa,
            })

    # 2. Suma dels productes parcials (si hi ha 2 o 3 files, es fa columna a columna; si n'hi ha 1, ja és el producte)
    digits_suma_parcials = []
    portades_suma_parcials = []

    if n_files_mult == 1:
        digits_suma_parcials = list(files_parcials[0])
        while len(digits_suma_parcials) > 1 and digits_suma_parcials[-1] == 0:
            digits_suma_parcials.pop()
    else:
        valors_per_fila = []
        max_len = 0
        for idx_f, digits in enumerate(files_parcials):
            alineats = ([0] * idx_f) + list(digits)
            valors_per_fila.append(alineats)
            max_len = max(max_len, len(alineats))

        for alineats in valors_per_fila:
            while len(alineats) < max_len:
                alineats.append(0)

        portades_suma_parcials = [0] * max_len
        portada_s = 0

        for col in range(max_len):
            sumands_col = [valors_per_fila[f][col] for f in range(n_files_mult)]
            total_col = sum(sumands_col) + portada_s
            xifra_s = total_col % 10
            portada_s_nova = total_col // 10

            digits_suma_parcials.append(xifra_s)
            portades_suma_parcials[col] = portada_s_nova

            detall_sumands = " + ".join(str(v) for v in sumands_col)
            nom_col = noms_posicio[col] if col < len(noms_posicio) else f"columna {col + 1}"

            if portada_s > 0:
                exp_s = (
                    f"Prova — suma dels productes parcials ({nom_col}): sumem {detall_sumands} "
                    f"més la portada {portada_s} = {total_col}. Posem {xifra_s}"
                    + (f" i ens emportem {portada_s_nova}." if portada_s_nova > 0 else ".")
                )
            else:
                exp_s = (
                    f"Prova — suma dels productes parcials ({nom_col}): sumem {detall_sumands} = {total_col}. "
                    f"Posem {xifra_s}" + (f" i ens emportem {portada_s_nova}." if portada_s_nova > 0 else ".")
                )

            passos_prova.append({
                "tipus": "prova_suma_parcials",
                "valor_actual": quocient,
                "divisor": divisor,
                "xifra_baixada": None,
                "xifra_q": None,
                "dd": None,
                "idx_fila": None,
                "pos_q": None,
                "col_suma": col,
                "producte_base": None,
                "portada_entrant": portada_s,
                "total": total_col,
                "xifra_res": xifra_s,
                "portada_nova": portada_s_nova,
                "producte": None,
                "residu_pas": residu,
                "col_inici": 0,
                "col_fi": len(str(dividend)) - 1,
                "col_baixada": None,
                "quocient_digits": list(quocient_digits),
                "quocient_parcial": quocient,
                "files_calcul": [dict(f) for f in files_calcul_previes],
                "residu_final": residu,
                "prova": {
                    "fase": "sumant_parcials",
                    "dividend": dividend,
                    "divisor": divisor,
                    "quocient": quocient,
                    "residu": residu,
                    "files_parcials": [list(f) for f in files_parcials],
                    "portades_sortida": [list(p) for p in portades_sortida],
                    "digits_suma_parcials": list(digits_suma_parcials),
                    "portades_suma_parcials": list(portades_suma_parcials),
                    "producte_quocient_divisor": None,
                    "digits_suma_residu": [],
                    "portades_suma_residu": [],
                    "total_amb_residu": None,
                    "es_exacta": residu == 0,
                },
                "explicacio": exp_s,
            })

            portada_s = portada_s_nova

        if portada_s > 0:
            digits_suma_parcials.append(portada_s)
            nom_col_extra = noms_posicio[max_len] if max_len < len(noms_posicio) else f"columna {max_len + 1}"
            passos_prova.append({
                "tipus": "prova_suma_parcials",
                "valor_actual": quocient,
                "divisor": divisor,
                "xifra_baixada": None,
                "xifra_q": None,
                "dd": None,
                "idx_fila": None,
                "pos_q": None,
                "col_suma": max_len,
                "producte_base": None,
                "portada_entrant": portada_s,
                "total": portada_s,
                "xifra_res": portada_s,
                "portada_nova": 0,
                "producte": None,
                "residu_pas": residu,
                "col_inici": 0,
                "col_fi": len(str(dividend)) - 1,
                "col_baixada": None,
                "quocient_digits": list(quocient_digits),
                "quocient_parcial": quocient,
                "files_calcul": [dict(f) for f in files_calcul_previes],
                "residu_final": residu,
                "prova": {
                    "fase": "sumant_parcials",
                    "dividend": dividend,
                    "divisor": divisor,
                    "quocient": quocient,
                    "residu": residu,
                    "files_parcials": [list(f) for f in files_parcials],
                    "portades_sortida": [list(p) for p in portades_sortida],
                    "digits_suma_parcials": list(digits_suma_parcials),
                    "portades_suma_parcials": list(portades_suma_parcials),
                    "producte_quocient_divisor": None,
                    "digits_suma_residu": [],
                    "portades_suma_residu": [],
                    "total_amb_residu": None,
                    "es_exacta": residu == 0,
                },
                "explicacio": f"Prova — suma dels productes parcials ({nom_col_extra}): baixem la portada {portada_s}.",
            })

        while len(digits_suma_parcials) > 1 and digits_suma_parcials[-1] == 0:
            digits_suma_parcials.pop()

    producte_qd = int("".join(str(d) for d in reversed(digits_suma_parcials))) if digits_suma_parcials else quocient * divisor

    # 3. Suma del residu pas a pas i comprovació final amb el dividend
    digits_prod_rev = [int(ch) for ch in reversed(str(producte_qd))]
    digits_res_rev = [int(ch) for ch in reversed(str(residu))] if residu > 0 else [0]
    n_cols_res = max(len(digits_prod_rev), len(digits_res_rev))

    while len(digits_prod_rev) < n_cols_res:
        digits_prod_rev.append(0)
    while len(digits_res_rev) < n_cols_res:
        digits_res_rev.append(0)

    digits_suma_residu = []
    portades_suma_residu = [0] * n_cols_res
    portada_r = 0

    for col in range(n_cols_res):
        dp = digits_prod_rev[col]
        dr = digits_res_rev[col]
        total_r = dp + dr + portada_r
        xifra_r = total_r % 10
        portada_r_nova = total_r // 10

        digits_suma_residu.append(xifra_r)
        portades_suma_residu[col] = portada_r_nova

        nom_col = noms_posicio[col] if col < len(noms_posicio) else f"columna {col + 1}"
        if residu == 0:
            exp_r = (
                f"Prova — residu 0 ({nom_col}): Quocient × Divisor té {dp} a les {nom_col} "
                f"i sumem 0 del residu → {xifra_r}."
            )
        elif portada_r > 0:
            exp_r = (
                f"Prova — sumem el residu ({nom_col}): fem {dp} + {dr} més la portada {portada_r} = {total_r}. "
                f"Posem {xifra_r}" + (f" i ens emportem {portada_r_nova}." if portada_r_nova > 0 else ".")
            )
        else:
            exp_r = (
                f"Prova — sumem el residu ({nom_col}): fem {dp} + {dr} = {total_r}. "
                f"Posem {xifra_r}" + (f" i ens emportem {portada_r_nova}." if portada_r_nova > 0 else ".")
            )

        passos_prova.append({
            "tipus": "prova_suma_residu_pas",
            "valor_actual": producte_qd,
            "divisor": divisor,
            "xifra_baixada": None,
            "xifra_q": None,
            "dd": None,
            "idx_fila": None,
            "pos_q": None,
            "col_suma": col,
            "producte_base": dp,
            "portada_entrant": portada_r,
            "total": total_r,
            "xifra_res": xifra_r,
            "portada_nova": portada_r_nova,
            "producte": producte_qd,
            "residu_pas": residu,
            "col_inici": 0,
            "col_fi": len(str(dividend)) - 1,
            "col_baixada": None,
            "quocient_digits": list(quocient_digits),
            "quocient_parcial": quocient,
            "files_calcul": [dict(f) for f in files_calcul_previes],
            "residu_final": residu,
            "prova": {
                "fase": "sumant_residu",
                "dividend": dividend,
                "divisor": divisor,
                "quocient": quocient,
                "residu": residu,
                "files_parcials": [list(f) for f in files_parcials],
                "portades_sortida": [list(p) for p in portades_sortida],
                "digits_suma_parcials": list(digits_suma_parcials),
                "portades_suma_parcials": list(portades_suma_parcials),
                "producte_quocient_divisor": producte_qd,
                "digits_suma_residu": list(digits_suma_residu),
                "portades_suma_residu": list(portades_suma_residu),
                "total_amb_residu": None,
                "es_exacta": residu == 0,
            },
            "explicacio": exp_r,
        })

        portada_r = portada_r_nova

    if portada_r > 0:
        digits_suma_residu.append(portada_r)
        nom_col_extra = noms_posicio[n_cols_res] if n_cols_res < len(noms_posicio) else f"columna {n_cols_res + 1}"
        passos_prova.append({
            "tipus": "prova_suma_residu_pas",
            "valor_actual": producte_qd,
            "divisor": divisor,
            "xifra_baixada": None,
            "xifra_q": None,
            "dd": None,
            "idx_fila": None,
            "pos_q": None,
            "col_suma": n_cols_res,
            "producte_base": 0,
            "portada_entrant": portada_r,
            "total": portada_r,
            "xifra_res": portada_r,
            "portada_nova": 0,
            "producte": producte_qd,
            "residu_pas": residu,
            "col_inici": 0,
            "col_fi": len(str(dividend)) - 1,
            "col_baixada": None,
            "quocient_digits": list(quocient_digits),
            "quocient_parcial": quocient,
            "files_calcul": [dict(f) for f in files_calcul_previes],
            "residu_final": residu,
            "prova": {
                "fase": "sumant_residu",
                "dividend": dividend,
                "divisor": divisor,
                "quocient": quocient,
                "residu": residu,
                "files_parcials": [list(f) for f in files_parcials],
                "portades_sortida": [list(p) for p in portades_sortida],
                "digits_suma_parcials": list(digits_suma_parcials),
                "portades_suma_parcials": list(portades_suma_parcials),
                "producte_quocient_divisor": producte_qd,
                "digits_suma_residu": list(digits_suma_residu),
                "portades_suma_residu": list(portades_suma_residu),
                "total_amb_residu": None,
                "es_exacta": residu == 0,
            },
            "explicacio": f"Prova — sumem el residu ({nom_col_extra}): baixem la portada {portada_r}.",
        })

    digits_final_nets = list(digits_suma_residu)
    while len(digits_final_nets) > 1 and digits_final_nets[-1] == 0:
        digits_final_nets.pop()

    total_amb_residu = int("".join(str(d) for d in reversed(digits_final_nets))) if digits_final_nets else producte_qd + residu

    if residu > 0:
        exp_fi = (
            f"Prova completada! {producte_qd} + {residu} = {total_amb_residu}, "
            f"que és exactament igual al dividend ({dividend})."
        )
    else:
        exp_fi = (
            f"Prova completada! Sense residu, {producte_qd} + 0 = {total_amb_residu}, "
            f"que és exactament igual al dividend ({dividend})."
        )

    passos_prova.append({
        "tipus": "prova_completada",
        "valor_actual": total_amb_residu,
        "divisor": divisor,
        "xifra_baixada": None,
        "xifra_q": None,
        "dd": None,
        "idx_fila": None,
        "pos_q": None,
        "col_suma": None,
        "producte_base": None,
        "portada_entrant": residu,
        "total": total_amb_residu,
        "xifra_res": None,
        "portada_nova": 0,
        "producte": producte_qd,
        "residu_pas": residu,
        "col_inici": 0,
        "col_fi": len(str(dividend)) - 1,
        "col_baixada": None,
        "quocient_digits": list(quocient_digits),
        "quocient_parcial": quocient,
        "files_calcul": [dict(f) for f in files_calcul_previes],
        "residu_final": residu,
        "prova": {
            "fase": "completada",
            "dividend": dividend,
            "divisor": divisor,
            "quocient": quocient,
            "residu": residu,
            "files_parcials": [list(f) for f in files_parcials],
            "portades_sortida": [list(p) for p in portades_sortida],
            "digits_suma_parcials": list(digits_suma_parcials),
            "portades_suma_parcials": list(portades_suma_parcials),
            "producte_quocient_divisor": producte_qd,
            "digits_suma_residu": list(digits_suma_residu),
            "portades_suma_residu": list(portades_suma_residu),
            "total_amb_residu": total_amb_residu,
            "es_exacta": residu == 0,
        },
        "explicacio": exp_fi,
    })

    return passos_prova


def _construir_passos_divisio(dividend, divisor):
    """
    Construeix la llista ordenada de passos per explicar la divisió
    amb el mètode de la caixa, incloent-hi el pas intermedi de baixar cada
    xifra del dividend i, al final, la prova de la divisió pas a pas.
    """
    digits_div = [int(ch) for ch in str(dividend)]
    n_digits = len(digits_div)

    passos = []
    quocient_digits = []
    files_calcul = []

    idx = 0
    valor_actual = 0
    col_inici_grup = 0
    primer_grup = True

    while idx < n_digits:
        if primer_grup:
            col_inici_grup = idx
            valor_actual = digits_div[idx]
            while idx + 1 < n_digits and valor_actual < divisor:
                idx += 1
                valor_actual = valor_actual * 10 + digits_div[idx]
            primer_grup = False
        else:
            residu_anterior = valor_actual
            xifra_baixada = digits_div[idx]
            valor_actual = residu_anterior * 10 + xifra_baixada

            if files_calcul and files_calcul[-1]["col_fi"] == idx - 1:
                files_calcul[-1] = {
                    "text": str(valor_actual),
                    "col_fi": idx,
                    "es_residu_final": False,
                    "es_baixada": True,
                }
            else:
                files_calcul.append({
                    "text": str(valor_actual),
                    "col_fi": idx,
                    "es_residu_final": False,
                    "es_baixada": True,
                })

            exp_baixar = (
                f"Baixem el {xifra_baixada} del dividend"
                + (f" al costat del residu {residu_anterior}" if residu_anterior > 0 else "")
                + f" i formem el {valor_actual}."
            )
            passos.append({
                "tipus": "baixa_xifra",
                "valor_actual": valor_actual,
                "divisor": divisor,
                "xifra_baixada": xifra_baixada,
                "xifra_q": None,
                "producte": None,
                "residu_pas": None,
                "col_inici": col_inici_grup,
                "col_fi": idx,
                "col_baixada": idx,
                "quocient_digits": list(quocient_digits),
                "quocient_parcial": int("".join(str(d) for d in quocient_digits)) if quocient_digits else 0,
                "files_calcul": [dict(f) for f in files_calcul],
                "residu_final": None,
                "prova": None,
                "explicacio": exp_baixar,
            })

        xifra_q = valor_actual // divisor
        producte = xifra_q * divisor
        residu_pas = valor_actual - producte
        quocient_digits.append(xifra_q)

        files_calcul.append({
            "text": str(residu_pas),
            "col_fi": idx,
            "es_residu_final": False,
            "es_baixada": False,
        })

        if residu_pas == 0:
            exp = (
                f"Dividim {valor_actual} entre {divisor}: busquem quin nombre multiplicat per {divisor} "
                f"s'acosta més sense passar-se. És {xifra_q} ({xifra_q} × {divisor} = {producte}). "
                f"Fem {valor_actual} − {producte} = 0 (sense residu en aquest pas)."
            )
        else:
            exp = (
                f"Dividim {valor_actual} entre {divisor}: busquem quin nombre multiplicat per {divisor} "
                f"s'acosta més sense passar-se. És {xifra_q} ({xifra_q} × {divisor} = {producte}). "
                f"Fem {valor_actual} − {producte} = {residu_pas} de residu."
            )

        quocient_parcial = int("".join(str(d) for d in quocient_digits))

        passos.append({
            "tipus": "divisio_pas",
            "valor_actual": valor_actual,
            "divisor": divisor,
            "xifra_baixada": None,
            "xifra_q": xifra_q,
            "producte": producte,
            "residu_pas": residu_pas,
            "col_inici": col_inici_grup,
            "col_fi": idx,
            "col_baixada": None,
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

    passos_prova = _construir_passos_prova_divisio(
        dividend=dividend,
        divisor=divisor,
        quocient=quocient_final,
        residu=residu_final,
        files_calcul_previes=files_calcul,
        quocient_digits=quocient_digits,
    )
    passos.extend(passos_prova)

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