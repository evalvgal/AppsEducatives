"""
Concepte UDC — Model lògic, dades i generació de nombres.
"""

import random

class ConcepteUDCModel:
    def __init__(self) -> None:
        self.generar_nuevo_numero()

    def generar_nuevo_numero(self) -> None:
        self.numero_actual = random.randint(100, 999)
        self.centenas = self.numero_actual // 100
        self.decenas = (self.numero_actual % 100) // 10
        self.unidades = self.numero_actual % 10