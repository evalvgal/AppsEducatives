"""
Model de dades i lògica matemàtica per a l'aplicació de Multiplicacions amb Portades.
Gestiona la generació aleatòria de nombres per a multiplicacions per 1, 2 i 3 xifres
amb portades assegurades i construeix la seqüència detallada de passos (productes parcials,
portades d'entrada i sortida, i suma final).
"""
import random


def _descompondre_xifres_dreta_a_esquerra(nombre):
    """
    Retorna les xifres d'un nombre de dreta a esquerra (unitats, desenes, centenes...).
    Exemple: 348 -> [8, 4, 3]
    """
    return [int(ch) for ch in reversed(str(nombre))]


def _te_portades(x, multiplicador):
    """Comprova si multiplicar x per cada xifra del multiplicador genera alguna portada."""
    xifres_x = _descompondre_xifres_dreta_a_esquerra(x)
    xifres_m = _descompondre_xifres_dreta_a_esquerra(multiplicador)

    for dm in xifres_m:
        portada = 0
        for dx in xifres_x:
            total = dx * dm + portada
            if total >= 10:
                return True
            portada = total // 10
    return False


def _construir_passos_multiplicacio(x, multiplicador):
    """
    Construeix la llista ordenada de passos per explicar la multiplicació amb portades.
    Cada pas és un diccionari amb informació gràfica i textual per a la vista.
    """
    xifres_x = _descompondre_xifres_dreta_a_esquerra(x)
    xifres_m = _descompondre_xifres_dreta_a_esquerra(multiplicador)
    n_files = len(xifres_m)

    # files_parcials[idx_fila] = llista de dígits col·locats de dreta a esquerra (posició 0 = unitats de la fila)
    files_parcials = [[] for _ in range(n_files)]
    # portades_sortida[idx_fila][pos_x] = portada generada en aquell pas (0 si no n'hi ha)
    portades_sortida = [[0] * len(xifres_x) for _ in range(n_files)]
    # portades_actives[idx_fila] = portada vigent que cal sumar al següent dígit de x
    portades_actives = [0 for _ in range(n_files)]

    passos = []
    noms_posicio = ["unitats", "desenes", "centenes", "unitats de miler", "desenes de miler", "centenes de miler"]
    noms_multiplicador = ["unitats", "desenes", "centenes"]

    for idx_fila, dm in enumerate(xifres_m):
        portada_entrant = 0
        nom_m = noms_multiplicador[idx_fila] if idx_fila < len(noms_multiplicador) else f"posició {idx_fila + 1}"

        for pos_x, dx in enumerate(xifres_x):
            nom_x = noms_posicio[pos_x] if pos_x < len(noms_posicio) else f"posició {pos_x + 1}"
            producte_base = dx * dm
            total = producte_base + portada_entrant
            xifra_resultat = total % 10
            portada_nova = total // 10

            files_parcials[idx_fila].append(xifra_resultat)
            portades_sortida[idx_fila][pos_x] = portada_nova
            portades_actives[idx_fila] = portada_nova

            if portada_entrant > 0:
                explicacio = (
                    f"Fila de les {nom_m} (multiplicant per {dm}): fem {dx} ({nom_x}) × {dm} = {producte_base}, "
                    f"hi sumem la portada {portada_entrant} → {total}. Escrivim {xifra_resultat}"
                    + (f" i ens emportem {portada_nova}." if portada_nova > 0 else ".")
                )
            else:
                explicacio = (
                    f"Fila de les {nom_m} (multiplicant per {dm}): fem {dx} ({nom_x}) × {dm} = {producte_base}. "
                    f"Escrivim {xifra_resultat}"
                    + (f" i ens emportem {portada_nova}." if portada_nova > 0 else ".")
                )

            passos.append({
                "tipus": "producte_xifra",
                "idx_fila": idx_fila,
                "pos_x": pos_x,
                "dx": dx,
                "dm": dm,
                "producte_base": producte_base,
                "portada_entrant": portada_entrant,
                "total": total,
                "xifra_resultat": xifra_resultat,
                "portada_nova": portada_nova,
                "files_parcials": [list(f) for f in files_parcials],
                "portades_sortida": [list(p) for p in portades_sortida],
                "portades_actives": list(portades_actives),
                "suma_parcial_mostrada": None,
                "portades_suma": [],
                "explicacio": explicacio,
            })

            portada_entrant = portada_nova

        if portada_entrant > 0:
            pos_final = len(xifres_x)
            files_parcials[idx_fila].append(portada_entrant)
            portades_actives[idx_fila] = 0

            explicacio_final_fila = (
                f"Fila de les {nom_m}: com que no queden més xifres a {x}, baixem directament "
                f"la portada {portada_entrant} i obtenim el producte parcial {idx_fila + 1}."
            )
            passos.append({
                "tipus": "baixa_portada",
                "idx_fila": idx_fila,
                "pos_x": pos_final,
                "dx": None,
                "dm": dm,
                "producte_base": None,
                "portada_entrant": portada_entrant,
                "total": portada_entrant,
                "xifra_resultat": portada_entrant,
                "portada_nova": 0,
                "files_parcials": [list(f) for f in files_parcials],
                "portades_sortida": [list(p) for p in portades_sortida],
                "portades_actives": list(portades_actives),
                "suma_parcial_mostrada": None,
                "portades_suma": [],
                "explicacio": explicacio_final_fila,
            })

    resultat_final = 0
    if n_files == 1:
        digits_r = files_parcials[0]
        resultat_final = int("".join(str(d) for d in reversed(digits_r))) if digits_r else 0
    else:
        valors_per_fila = []
        max_len = 0
        for idx_fila, digits in enumerate(files_parcials):
            alineats = ([0] * idx_fila) + list(digits)
            valors_per_fila.append(alineats)
            max_len = max(max_len, len(alineats))

        for alineats in valors_per_fila:
            while len(alineats) < max_len:
                alineats.append(0)

        digits_suma = []
        portades_suma = [0] * max_len
        portada_s = 0

        for col in range(max_len):
            sumands_col = [valors_per_fila[f][col] for f in range(n_files)]
            total_col = sum(sumands_col) + portada_s
            xifra_s = total_col % 10
            portada_s_nova = total_col // 10

            digits_suma.append(xifra_s)
            portades_suma[col] = portada_s_nova

            detall_sumands = " + ".join(str(v) for v in sumands_col)
            nom_col = noms_posicio[col] if col < len(noms_posicio) else f"columna {col + 1}"

            if portada_s > 0:
                exp_suma = (
                    f"Suma final ({nom_col}): sumem {detall_sumands} més la portada {portada_s} = {total_col}. "
                    f"Posem {xifra_s}" + (f" i ens emportem {portada_s_nova}." if portada_s_nova > 0 else ".")
                )
            else:
                exp_suma = (
                    f"Suma final ({nom_col}): sumem {detall_sumands} = {total_col}. "
                    f"Posem {xifra_s}" + (f" i ens emportem {portada_s_nova}." if portada_s_nova > 0 else ".")
                )

            passos.append({
                "tipus": "suma_final",
                "idx_fila": None,
                "pos_x": col,
                "dx": None,
                "dm": None,
                "producte_base": None,
                "portada_entrant": portada_s,
                "total": total_col,
                "xifra_resultat": xifra_s,
                "portada_nova": portada_s_nova,
                "files_parcials": [list(f) for f in files_parcials],
                "portades_sortida": [list(p) for p in portades_sortida],
                "portades_actives": [0 for _ in range(n_files)],
                "suma_parcial_mostrada": list(digits_suma),
                "portades_suma": list(portades_suma),
                "explicacio": exp_suma,
            })

            portada_s = portada_s_nova

        if portada_s > 0:
            digits_suma.append(portada_s)
            nom_col_extra = (
                noms_posicio[max_len] if max_len < len(noms_posicio) else f"columna {max_len + 1}"
            )
            passos.append({
                "tipus": "suma_final",
                "idx_fila": None,
                "pos_x": max_len,
                "dx": None,
                "dm": None,
                "producte_base": None,
                "portada_entrant": portada_s,
                "total": portada_s,
                "xifra_resultat": portada_s,
                "portada_nova": 0,
                "files_parcials": [list(f) for f in files_parcials],
                "portades_sortida": [list(p) for p in portades_sortida],
                "portades_actives": [0 for _ in range(n_files)],
                "suma_parcial_mostrada": list(digits_suma),
                "portades_suma": list(portades_suma),
                "explicacio": f"Suma final ({nom_col_extra}): baixem la portada {portada_s}.",
            })

        digits_nets = list(digits_suma)
        while len(digits_nets) > 1 and digits_nets[-1] == 0:
            digits_nets.pop()

        resultat_final = int("".join(str(d) for d in reversed(digits_nets))) if digits_nets else x * multiplicador

    return {
        "x": x,
        "multiplicador": multiplicador,
        "resultat_final": resultat_final,
        "passos": passos,
    }


def generar_exercici_multiplicacio(xifres_multiplicador, ultim_exercici=None):
    """
    Genera un exercici aleatori de multiplicació amb portades:
    - xifres_multiplicador = 1: x en [1..999], y en [1..9]
    - xifres_multiplicador = 2: x en [1..999], yz amb y, z en [1..9]
    - xifres_multiplicador = 3: x en [1..999], yzm amb y, z, m en [1..9]
    """
    if xifres_multiplicador not in (1, 2, 3):
        raise ValueError("xifres_multiplicador ha de ser 1, 2 o 3.")

    for _ in range(500):
        x = random.randint(1, 999)

        if xifres_multiplicador == 1:
            mult = random.randint(1, 9)
        elif xifres_multiplicador == 2:
            y = random.randint(1, 9)
            z = random.randint(1, 9)
            mult = y * 10 + z
        else:
            y = random.randint(1, 9)
            z = random.randint(1, 9)
            m = random.randint(1, 9)
            mult = y * 100 + z * 10 + m

        if ultim_exercici == (x, mult):
            continue

        if _te_portades(x, mult):
            dades = _construir_passos_multiplicacio(x, mult)
            dades["xifres_multiplicador"] = xifres_multiplicador
            return dades

    x = 248
    mult = 6 if xifres_multiplicador == 1 else (34 if xifres_multiplicador == 2 else 126)
    dades = _construir_passos_multiplicacio(x, mult)
    dades["xifres_multiplicador"] = xifres_multiplicador
    return dades