"""
La Regla Pnemotècnica del DUC — Model lògic, dades i descomposició.
"""

import random

# Colors per a la descomposició de text
COLOR_TEXTO = (50, 40, 80)
COLOR_CENTENA = (230, 170, 120)
COLOR_DECENA = (120, 170, 230)
COLOR_UNIDAD = (100, 210, 140)

def obtenir_parts_text_cat(n: int) -> list:
    """Retorna una llista de tuples (text, color) amb la descomposició en català."""
    unidades_dict = {
        1: "un", 2: "dos", 3: "tres", 4: "quatre", 5: "cinc",
        6: "sis", 7: "set", 8: "vuit", 9: "nou"
    }
    decenas_dict = {
        1: "deu", 2: "vint", 3: "trenta", 4: "quaranta", 5: "cinquanta",
        6: "seixanta", 7: "setanta", 8: "vuitanta", 9: "noranta"
    }
    especiales_diez = {
        11: "onze", 12: "dotze", 13: "tretze", 14: "quatorze",
        15: "quinze", 16: "setze", 17: "disset", 18: "divuit", 19: "dinou"
    }
    
    c = n // 100
    d = (n % 100) // 10
    u = n % 10
    resto = n % 100
    
    parts = []
    
    if c > 0:
        if c == 1:
            parts.append(("cent", COLOR_CENTENA))
        else:
            parts.append((f"{unidades_dict[c]}-cents", COLOR_CENTENA))
            
    if resto == 0:
        return parts
        
    if c > 0:
        parts.append((" ", COLOR_TEXTO))
        
    if resto in especiales_diez:
        parts.append((especiales_diez[resto], COLOR_DECENA))
    else:
        if d > 0:
            parts.append((decenas_dict[d], COLOR_DECENA))
            if u > 0:
                if d == 2:
                    parts.append(("-i-", COLOR_TEXTO))
                    parts.append((unidades_dict[u], COLOR_UNIDAD))
                else:
                    parts.append(("-", COLOR_TEXTO))
                    parts.append((unidades_dict[u], COLOR_UNIDAD))
        elif u > 0:
            parts.append((unidades_dict[u], COLOR_UNIDAD))
            
    return parts


class DUCModel:
    def __init__(self) -> None:
        self.numero_actual = 0
        self.centenas = 0
        self.decenas = 0
        self.unidades = 0
        self.parts_text = []
        self.estado_juego = 0
        self.generar_nuevo_numero()

    def generar_nuevo_numero(self) -> None:
        self.numero_actual = random.randint(100, 999)
        self.centenas = self.numero_actual // 100
        self.decenas = (self.numero_actual % 100) // 10
        self.unidades = self.numero_actual % 10
        self.parts_text = obtenir_parts_text_cat(self.numero_actual)
        self.estado_juego = 0

    def avanzar_estado(self) -> None:
        if self.estado_juego == 0:
            self.estado_juego = 1
        elif self.estado_juego == 1:
            self.estado_juego = 2