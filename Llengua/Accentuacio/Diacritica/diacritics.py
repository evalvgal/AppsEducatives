"""
Accents Diacrítics en Català — Model lògic.
"""

from diccionari_diacritics import PARELLS_DIACRITICS


class DiacriticsModel:
    def __init__(self) -> None:
        self.pagina_actual = 0
        self.total_pagines = len(PARELLS_DIACRITICS)

    @property
    def parell_actual(self) -> dict:
        return PARELLS_DIACRITICS[self.pagina_actual]

    def seguent_pagina(self) -> None:
        self.pagina_actual = (self.pagina_actual + 1) % self.total_pagines

    def anterior_pagina(self) -> None:
        self.pagina_actual = (self.pagina_actual - 1) % self.total_pagines

    def anar_a_pagina(self, idx: int) -> None:
        if 0 <= idx < self.total_pagines:
            self.pagina_actual = idx