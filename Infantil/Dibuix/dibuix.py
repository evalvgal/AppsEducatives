"""
Model lògic per a l'aplicació de Dibuix Animat per a Educació Infantil.
Inclou classificació automàtica (onades, caminar, botar o ma) i animació procedimental.
"""

import math
import random


class DibuixModel:
    def __init__(self) -> None:
        self.tracos: list[dict] = []
        self.tracos_desfets: list[dict] = []
        self.trac_actual: dict | None = None

        self.eina_activa = "LLAPIS"
        self.color_llapis = (35, 35, 45)  # Negre per defecte
        self.gruix_llapis = 12
        self.gruix_goma = 36

        self.animant = False
        self.temps_animacio = 0.0
        self.tipus_animacio_detectat = "botar"  # "onades", "caminar", "botar", "ma"
        self.particules: list[dict] = []
        
        # Variables per al moviment i rebot d'anada i tornada (caminar)
        self.x_transllacio = 0.0
        self.velocitat_x = 2.5
        self.direccio_x = 1  # 1 = cap a la dreta, -1 = cap a l'esquerra

    def seleccionar_llapis(self, color: tuple[int, int, int] | None = None) -> None:
        self.eina_activa = "LLAPIS"
        if color:
            self.color_llapis = color

    def seleccionar_goma(self) -> None:
        self.eina_activa = "GOMA"

    def iniciar_trac(self, pos: tuple[int, int], color_fons: tuple[int, int, int]) -> None:
        if self.animant:
            return
        es_goma = (self.eina_activa == "GOMA")
        self.trac_actual = {
            "punts": [pos],
            "color": color_fons if es_goma else self.color_llapis,
            "gruix": self.gruix_goma if es_goma else self.gruix_llapis,
            "es_goma": es_goma
        }

    def afegir_punt(self, pos: tuple[int, int]) -> None:
        if self.trac_actual is not None and not self.animant:
            if self.trac_actual["punts"][-1] != pos:
                self.trac_actual["punts"].append(pos)

    def finalitzar_trac(self) -> None:
        if self.trac_actual is not None:
            if len(self.trac_actual["punts"]) >= 1:
                self.tracos.append(self.trac_actual)
                self.tracos_desfets.clear()
            self.trac_actual = None

    def desfer(self) -> None:
        if not self.animant and self.tracos:
            ultim = self.tracos.pop()
            self.tracos_desfets.append(ultim)

    def refer(self) -> None:
        if not self.animant and self.tracos_desfets:
            recuperat = self.tracos_desfets.pop()
            self.tracos.append(recuperat)

    def netejar_tot(self) -> None:
        self.tracos.clear()
        self.tracos_desfets.clear()
        self.trac_actual = None
        self.animant = False
        self.temps_animacio = 0.0
        self.particules.clear()
        self.x_transllacio = 0.0
        self.direccio_x = 1

    def classificar_dibuix(self) -> str:
        """Heurística geomètrica per endevinar si són onades, persona, mà o objecte."""
        tots_punts = [p for t in self.tracos for p in t["punts"]]
        if not tots_punts:
            return "botar"

        min_x = min(p[0] for p in tots_punts)
        max_x = max(p[0] for p in tots_punts)
        min_y = min(p[1] for p in tots_punts)
        max_y = max(p[1] for p in tots_punts)

        ample = max_x - min_x
        alcada = max_y - min_y

        if ample == 0: ample = 1
        if alcada == 0: alcada = 1

        proporcio = ample / alcada

        if proporcio > 2.2:
            return "onades"      # Molt horitzontal -> Onades del mar
        elif proporcio < 0.75:
            return "caminar"     # Molt vertical -> Persona / Animal dret
        elif 0.8 <= proporcio <= 1.4:
            return "ma"          # Proporció equilibrada (quadrada) -> Mà amb dits
        else:
            return "botar"       # Altres objectes -> Botant

    def alternar_animacio(self, amplada: int, alcada: int) -> None:
        if not self.tracos:
            return
        self.animant = not self.animant
        self.temps_animacio = 0.0
        if self.animant:
            self.tipus_animacio_detectat = self.classificar_dibuix()
            self._generar_particules(amplada, alcada)
            self.x_transllacio = 0.0
            self.direccio_x = 1
        else:
            self.particules.clear()

    def actualitzar_animacio(self, dt: float, amplada: int, alcada: int) -> None:
        if not self.animant:
            return
        self.temps_animacio += dt

        if self.tipus_animacio_detectat == "caminar":
            tots_punts = [p for t in self.tracos for p in t["punts"]]
            min_x = min(p[0] for p in tots_punts)
            max_x = max(p[0] for p in tots_punts)
            ample_dibuix = max_x - min_x

            self.x_transllacio += self.velocitat_x * self.direccio_x

            if (min_x + self.x_transllacio) > (amplada - 80):
                self.direccio_x = -1
            elif (max_x + self.x_transllacio) < 80:
                self.direccio_x = 1

        for p in self.particules:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            if p["y"] < -20:
                p["y"] = alcada + 20
                p["x"] = random.randint(0, amplada)

    def _generar_particules(self, amplada: int, alcada: int) -> None:
        self.particules.clear()
        if self.tipus_animacio_detectat == "onades":
            colors = [(100, 200, 255), (50, 150, 220), (200, 230, 255)]
        elif self.tipus_animacio_detectat == "caminar":
            colors = [(255, 200, 50), (240, 120, 40), (255, 240, 150)]
        elif self.tipus_animacio_detectat == "ma":
            colors = [(255, 220, 177), (255, 180, 120), (255, 240, 200)]  # Tons càlids/pell
        else:
            colors = [(255, 120, 180), (155, 89, 182), (46, 204, 113)]

        for _ in range(45):
            self.particules.append({
                "x": random.randint(0, amplada),
                "y": random.randint(0, alcada),
                "vx": random.uniform(-0.8, 0.8),
                "vy": random.uniform(-2.5, -0.8),
                "radi": random.randint(5, 11),
                "color": random.choice(colors)
            })