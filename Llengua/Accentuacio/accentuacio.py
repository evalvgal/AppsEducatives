"""
Accenturació en Català — Model lògic amb importació del diccionari de dades.
"""

import random
from diccionari import NORMES_ACCENTUACIO, BANC_JOC_REALS


def treure_accent(paraula: str) -> str:
    reemplazos = {"à": "a", "è": "e", "é": "e", "í": "i", "ò": "o", "ó": "o", "ú": "u"}
    return "".join(reemplazos.get(c, c) for c in paraula)


class AccentuacioModel:
    def __init__(self) -> None:
        self.mode_actual = "normes"
        self.norma_index = 0
        self.joc_pas = 0  
        self.paraula_actual = None
        self._ultimes_paraules = []
        self.carregar_nova_paraula_joc()

    def canviar_mode(self, mode: str) -> None:
        self.mode_actual = mode
        if mode == "joc":
            self.carregar_nova_paraula_joc()

    def seguent_norma(self) -> None:
        self.norma_index = (self.norma_index + 1) % len(NORMES_ACCENTUACIO)

    def anterior_norma(self) -> None:
        self.norma_index = (self.norma_index - 1) % len(NORMES_ACCENTUACIO)

    @property
    def norma_actual_info(self) -> dict:
        return NORMES_ACCENTUACIO[self.norma_index]

    @property
    def paraula_sense_accent(self) -> str:
        if not self.paraula_actual:
            return ""
        return treure_accent(self.paraula_actual["paraula"]).upper()

    def carregar_nova_paraula_joc(self) -> None:
        opcions_disponibles = [p for p in BANC_JOC_REALS if p["paraula"] not in self._ultimes_paraules]
        if not opcions_disponibles:
            opcions_disponibles = BANC_JOC_REALS
            self._ultimes_paraules = []

        self.paraula_actual = random.choice(opcions_disponibles)
        
        self._ultimes_paraules.append(self.paraula_actual["paraula"])
        if len(self._ultimes_paraules) > 5:
            self._ultimes_paraules.pop(0)
            
        self.joc_pas = 0

    def avançar_pas_joc(main_self) -> None:
        if main_self.joc_pas < 3:
            main_self.joc_pas += 1
        else:
            main_self.carregar_nova_paraula_joc()