"""
Model lògic per a l'aplicació de Dibuix Animat per a Educació Infantil.
Inclou classificació automàtica per a onades, caminar, botar, mà, lletres, nombres i figures geomètriques.
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
        self.tipus_animacio_detectat = "botar"  # "onades", "caminar", "botar", "ma", "lletra", "figura"
        self.particules: list[dict] = []

        # Grups detectats quan hi ha 1 o més elements (lletres, nombres o figures)
        self.grups_personatges: list[list[dict]] = []

        # Variables per al moviment i rebot d'anada i tornada
        self.x_transllacio = 0.0
        self.velocitat_x = 2.8
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
        self.grups_personatges.clear()
        self.x_transllacio = 0.0
        self.direccio_x = 1

    def agrupar_elements(self) -> list[list[dict]]:
        """Agrupa els traços en caràcters o figures individuals segons la seva proximitat horitzontal."""
        tracos_valids = [t for t in self.tracos if not t.get("es_goma", False) and t["punts"]]
        if not tracos_valids:
            return []

        caixes = []
        for t in tracos_valids:
            xs = [p[0] for p in t["punts"]]
            ys = [p[1] for p in t["punts"]]
            caixes.append({
                "trac": t,
                "min_x": min(xs),
                "max_x": max(xs),
                "min_y": min(ys),
                "max_y": max(ys),
            })

        caixes.sort(key=lambda c: c["min_x"])

        grups: list[dict] = []
        marge_unio = 16

        for c in caixes:
            afegit = False
            for g in grups:
                solapament = min(g["max_x"], c["max_x"]) - max(g["min_x"], c["min_x"])
                ample_c = max(1, c["max_x"] - c["min_x"])
                if solapament > -marge_unio and (solapament >= ample_c * 0.25 or c["min_x"] <= g["max_x"] + 5):
                    g["tracos"].append(c["trac"])
                    g["min_x"] = min(g["min_x"], c["min_x"])
                    g["max_x"] = max(g["max_x"], c["max_x"])
                    g["min_y"] = min(g["min_y"], c["min_y"])
                    g["max_y"] = max(g["max_y"], c["max_y"])
                    afegit = True
                    break

            if not afegit:
                grups.append({
                    "tracos": [c["trac"]],
                    "min_x": c["min_x"],
                    "max_x": c["max_x"],
                    "min_y": c["min_y"],
                    "max_y": c["max_y"],
                })

        return [g["tracos"] for g in grups]

    def _es_figura_tancada(self, grup: list[dict]) -> bool:
        """Comprova si un grup de traços forma una figura geomètriques tancada."""
        punts = [p for t in grup for p in t["punts"]]
        if len(punts) < 8:
            return False

        min_x = min(p[0] for p in punts)
        max_x = max(p[0] for p in punts)
        min_y = min(p[1] for p in punts)
        max_y = max(p[1] for p in punts)
        diagonal = math.hypot(max_x - min_x, max_y - min_y)
        if diagonal < 60:
            return False

        inici = punts[0]
        final = punts[-1]
        dist_extrems = math.hypot(final[0] - inici[0], final[1] - inici[1])

        return dist_extrems <= diagonal * 0.32

    def classificar_dibuix(self) -> str:
        """Heurística geomètrica per endevinar el tipus d'animació."""
        tracos_valids = [t for t in self.tracos if not t.get("es_goma", False)]
        tots_punts = [p for t in tracos_valids for p in t["punts"]]
        if not tots_punts:
            return "botar"

        min_x = min(p[0] for p in tots_punts)
        max_x = max(p[0] for p in tots_punts)
        min_y = min(p[1] for p in tots_punts)
        max_y = max(p[1] for p in tots_punts)

        ample = max(1, max_x - min_x)
        alcada = max(1, max_y - min_y)
        proporcio = ample / alcada
        num_tracos = len(tracos_valids)

        grups = self.agrupar_elements()

        # 1. Figures geomètriques tancades
        if grups:
            totes_tancades = all(self._es_figura_tancada(g) and len(g) <= 4 for g in grups)
            if totes_tancades:
                return "figura"

        # 2. Lletres (A-Z) o Nombres (0-9)
        if len(grups) >= 2:
            tots_son_caracters = all(
                len(g) <= 3 and (max(1, max(p[1] for t in g for p in t["punts"]) - min(p[1] for t in g for p in t["punts"])) >= 65)
                for g in grups
            )
            if tots_son_caracters:
                return "lletra"

        if num_tracos <= 3 and 0.40 <= proporcio <= 1.30 and alcada >= 75:
            return "lletra"

        # 3. Altres dibuixos
        if proporcio > 2.2:
            return "onades"
        elif proporcio < 0.75:
            return "caminar"
        elif 0.8 <= proporcio <= 1.4:
            return "ma"
        else:
            return "botar"

    def alternar_animacio(self, amplada: int, alcada: int, forcar_tipus: str | None = None) -> None:
        if not self.tracos:
            return
        if forcar_tipus:
            self.animant = True
            self.temps_animacio = 0.0
            self.tipus_animacio_detectat = forcar_tipus
            self.grups_personatges = self.agrupar_elements() if forcar_tipus in ("lletra", "figura") else []
            self._generar_particules(amplada, alcada)
            self.x_transllacio = 0.0
            self.direccio_x = 1
            return

        self.animant = not self.animant
        self.temps_animacio = 0.0
        if self.animant:
            self.tipus_animacio_detectat = self.classificar_dibuix()
            self.grups_personatges = self.agrupar_elements() if self.tipus_animacio_detectat in ("lletra", "figura") else []
            self._generar_particules(amplada, alcada)
            self.x_transllacio = 0.0
            self.direccio_x = 1
        else:
            self.particules.clear()
            self.grups_personatges.clear()

    def actualitzar_animacio(self, dt: float, amplada: int, alcada: int) -> None:
        if not self.animant:
            return
        self.temps_animacio += dt

        if self.tipus_animacio_detectat in ("caminar", "lletra", "figura"):
            tots_punts = [p for t in self.tracos for p in t["punts"]]
            if tots_punts:
                min_x = min(p[0] for p in tots_punts)
                max_x = max(p[0] for p in tots_punts)

                self.x_transllacio += self.velocitat_x * self.direccio_x

                if (max_x + self.x_transllacio) > (amplada - 90):
                    self.direccio_x = -1
                elif (min_x + self.x_transllacio) < 90:
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
            colors = [(255, 220, 177), (255, 180, 120), (255, 240, 200)]
        elif self.tipus_animacio_detectat in ("lletra", "figura"):
            colors = [(100, 220, 150), (90, 170, 255), (255, 210, 80)]
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