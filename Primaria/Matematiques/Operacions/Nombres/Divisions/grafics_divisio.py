"""
Vista gràfica amb Pygame per a l'aplicació de Divisions.
Gestiona el menú de 3 parts (divisor d'1, 2 i 3 xifres), el mètode gràfic
de la caixa amb pas a pas, l'explicació textual sincronitzada i la prova
de la divisió.
"""
import pygame


class VistaDivisio:
    def __init__(self):
        pygame.init()

        info = pygame.display.Info()
        self.amplada = info.current_w if info.current_w > 0 else 1280
        self.alcada = info.current_h if info.current_h > 0 else 800

        self.pantalla_completa = True
        self.pantalla = pygame.display.set_mode((self.amplada, self.alcada), pygame.FULLSCREEN)
        pygame.display.set_caption("Divisions Pas a Pas - Educació Primària")

        self.rellotge = pygame.time.Clock()

        # Paleta educativa clara i accessible
        self.BLANC = (255, 255, 255)
        self.FONS = (242, 247, 252)
        self.CAIXA = (255, 255, 255)
        self.VORA = (195, 207, 220)
        self.TEXT = (33, 47, 61)
        self.TEXT_SUAU = (100, 116, 139)

        self.BLAU = (41, 128, 185)
        self.BLAU_HOVER = (84, 153, 199)
        self.VERD = (39, 174, 96)
        self.VERD_HOVER = (82, 190, 128)
        self.TARONJA = (230, 126, 34)
        self.TARONJA_HOVER = (240, 150, 68)
        self.LILA = (142, 68, 173)
        self.LILA_HOVER = (165, 105, 189)
        self.VERMELL = (231, 76, 60)
        self.VERMELL_HOVER = (236, 112, 99)
        self.GRIS_BOTO = (213, 219, 226)
        self.GRIS_HOVER = (195, 203, 212)

        self._carregar_fonts()

    def _carregar_fonts(self):
        escala = min(self.amplada / 1440.0, self.alcada / 900.0)
        escala = max(0.75, min(escala, 1.35))

        m_titol = int(42 * escala)
        m_mitjana = int(27 * escala)
        m_text = int(20 * escala)
        m_petita = int(16 * escala)
        m_xifra = int(34 * escala)

        try:
            self.font_titol = pygame.font.SysFont("Arial", m_titol, bold=True)
            self.font_mitjana = pygame.font.SysFont("Arial", m_mitjana, bold=True)
            self.font_text = pygame.font.SysFont("Arial", m_text)
            self.font_text_negreta = pygame.font.SysFont("Arial", m_text, bold=True)
            self.font_petita = pygame.font.SysFont("Arial", m_petita, bold=True)
            self.font_xifra = pygame.font.SysFont("Arial", m_xifra, bold=True)
        except Exception:
            self.font_titol = pygame.font.Font(None, m_titol + 6)
            self.font_mitjana = pygame.font.Font(None, m_mitjana + 4)
            self.font_text = pygame.font.Font(None, m_text + 4)
            self.font_text_negreta = pygame.font.Font(None, m_text + 4)
            self.font_petita = pygame.font.Font(None, m_petita + 4)
            self.font_xifra = pygame.font.Font(None, m_xifra + 6)

    def alternar_pantalla_completa(self):
        self.pantalla_completa = not self.pantalla_completa
        if self.pantalla_completa:
            info = pygame.display.Info()
            self.amplada = info.current_w if info.current_w > 0 else 1280
            self.alcada = info.current_h if info.current_h > 0 else 800
            self.pantalla = pygame.display.set_mode((self.amplada, self.alcada), pygame.FULLSCREEN)
        else:
            self.amplada = 1280
            self.alcada = 800
            self.pantalla = pygame.display.set_mode((self.amplada, self.alcada), pygame.RESIZABLE)
        self._carregar_fonts()

    def gestionar_redimensio(self, nova_amplada, nova_alcada):
        if not self.pantalla_completa:
            self.amplada = max(920, nova_amplada)
            self.alcada = max(680, nova_alcada)
            self.pantalla = pygame.display.set_mode((self.amplada, self.alcada), pygame.RESIZABLE)
            self._carregar_fonts()

    def obtenir_rect_sortir(self):
        return pygame.Rect(self.amplada - 150, 22, 125, 48)

    def _dibuixar_boto(self, rect, text, color_base, color_hover, font=None, color_text=None):
        font_usada = font or self.font_mitjana
        color_txt = color_text or self.BLANC
        pos_ratoli = pygame.mouse.get_pos()

        sobre = rect.collidepoint(pos_ratoli)
        r_dib = rect.inflate(8, 8) if sobre else rect
        color = color_hover if sobre else color_base

        pygame.draw.rect(self.pantalla, color, r_dib, border_radius=14)
        surf = font_usada.render(text, True, color_txt)
        self.pantalla.blit(surf, surf.get_rect(center=r_dib.center))
        return rect

    def _pintar_capcalera(self, titol):
        self.pantalla.fill(self.FONS)
        txt_titol = self.font_titol.render(titol, True, self.TEXT)
        self.pantalla.blit(txt_titol, (40, 22))
        self._dibuixar_boto(
            self.obtenir_rect_sortir(),
            "Sortir",
            self.VERMELL,
            self.VERMELL_HOVER,
            font=self.font_mitjana,
        )

    def _dibuixar_peu_navegacio(self, te_enrere=True, text_enrere="← Menú principal", botons_extra=None):
        rects = {}
        y_peu = self.alcada - 74

        if te_enrere:
            r_enrere = pygame.Rect(40, y_peu, 220, 50)
            self._dibuixar_boto(
                r_enrere,
                text_enrere,
                self.GRIS_BOTO,
                self.GRIS_HOVER,
                font=self.font_text_negreta,
                color_text=self.TEXT,
            )
            rects["enrere"] = r_enrere

        if botons_extra:
            ample_b = 240
            espai = 20
            total = len(botons_extra) * ample_b + (len(botons_extra) - 1) * espai
            x_actual = self.amplada - 40 - total
            for clau, text, c_base, c_hover in botons_extra:
                r_b = pygame.Rect(x_actual, y_peu, ample_b, 50)
                self._dibuixar_boto(r_b, text, c_base, c_hover, font=self.font_text_negreta)
                rects[clau] = r_b
                x_actual += ample_b + espai

        return rects

    def _renderitzar_text_ajustat(self, text, font, color, x, y, max_ample, interlineat=5):
        """Renderitza text dividit en línies i retorna la coordenada Y final."""
        paraules = text.split(" ")
        linia = []
        y_act = y

        for paraula in paraules:
            prova = " ".join(linia + [paraula])
            if font.size(prova)[0] <= max_ample:
                linia.append(paraula)
            else:
                surf = font.render(" ".join(linia), True, color)
                self.pantalla.blit(surf, (x, y_act))
                y_act += font.get_linesize() + interlineat
                linia = [paraula]

        if linia:
            surf = font.render(" ".join(linia), True, color)
            self.pantalla.blit(surf, (x, y_act))
            y_act += font.get_linesize() + interlineat

        return y_act

    def dibuixar_menu_principal(self):
        self._pintar_capcalera("Divisions Pas a Pas")

        cx = self.amplada // 2
        cy = self.alcada // 2
        w_boto = min(740, int(self.amplada * 0.74))
        h_boto = 88

        r_1 = pygame.Rect(cx - w_boto // 2, cy - 145, w_boto, h_boto)
        r_2 = pygame.Rect(cx - w_boto // 2, cy - 35, w_boto, h_boto)
        r_3 = pygame.Rect(cx - w_boto // 2, cy + 75, w_boto, h_boto)

        self._dibuixar_boto(r_1, "1. Divisions amb el divisor d'1 xifra", self.BLAU, self.BLAU_HOVER)
        self._dibuixar_boto(r_2, "2. Divisions amb el divisor de 2 xifres", self.VERD, self.VERD_HOVER)
        self._dibuixar_boto(r_3, "3. Divisions amb el divisor de 3 xifres", self.TARONJA, self.TARONJA_HOVER)

        return {"divisor_1": r_1, "divisor_2": r_2, "divisor_3": r_3}

    def _dibuixar_caixa_divisio(self, exercici, pas_actual, x_esq_zona, y_inici):
        """
        Dibuixa la divisió amb el mètode de la caixa:
        - Dividend a l'esquerra
        - Caixa del divisor a la dreta (línia vertical a l'esquerra i horitzontal a sota)
        - Quocient sota la caixa del divisor
        - Càlculs / residus alineats sota el dividend
        """
        str_div = str(exercici["dividend"])
        str_divisor = str(exercici["divisor"])
        n_digits = len(str_div)
        passos = exercici["passos"]
        pas = passos[pas_actual - 1] if pas_actual > 0 else None

        ample_col = 42
        alt_fila = 42

        # Coordenades de cada xifra del dividend
        centres_x = [x_esq_zona + i * ample_col + ample_col // 2 for i in range(n_digits)]
        y_dividend = y_inici + 8

        # Ressaltat del grup actiu del dividend durant un pas de divisió
        if pas and pas["tipus"] == "divisio_pas":
            x_g_esq = centres_x[pas["col_inici"]] - ample_col // 2 + 3
            x_g_drt = centres_x[pas["col_fi"]] + ample_col // 2 - 3
            r_grup = pygame.Rect(x_g_esq, y_dividend - 2, x_g_drt - x_g_esq, alt_fila)
            pygame.draw.rect(self.pantalla, (219, 234, 254), r_grup, border_radius=8)
            pygame.draw.rect(self.pantalla, self.BLAU, r_grup, 2, border_radius=8)

        # Dibuixem les xifres del dividend
        for i, ch in enumerate(str_div):
            es_actiu = pas is not None and pas["tipus"] == "divisio_pas" and pas["col_inici"] <= i <= pas["col_fi"]
            color_d = self.BLAU if es_actiu else self.TEXT
            surf_d = self.font_xifra.render(ch, True, color_d)
            self.pantalla.blit(surf_d, surf_d.get_rect(center=(centres_x[i], y_dividend + alt_fila // 2 - 2)))

        # Caixa del divisor a la dreta del dividend
        x_caixa_esq = x_esq_zona + n_digits * ample_col + 14
        ample_caixa = max(92, len(str_divisor) * 26 + 44)
        y_caixa_top = y_dividend - 4
        y_caixa_bottom = y_dividend + alt_fila + 2

        # Fons suau de la caixa del divisor
        pygame.draw.rect(
            self.pantalla,
            (250, 245, 255),
            pygame.Rect(x_caixa_esq, y_caixa_top, ample_caixa, y_caixa_bottom - y_caixa_top),
            border_top_right_radius=8,
        )
        # Línia vertical esquerra i línia horitzontal inferior de la caixa
        pygame.draw.line(self.pantalla, self.TEXT, (x_caixa_esq, y_caixa_top), (x_caixa_esq, y_caixa_bottom), 3)
        pygame.draw.line(
            self.pantalla,
            self.TEXT,
            (x_caixa_esq, y_caixa_bottom),
            (x_caixa_esq + ample_caixa, y_caixa_bottom),
            3,
        )

        # Divisor dins de la caixa
        surf_div = self.font_xifra.render(str_divisor, True, self.LILA)
        self.pantalla.blit(
            surf_div,
            surf_div.get_rect(center=(x_caixa_esq + ample_caixa // 2, (y_caixa_top + y_caixa_bottom) // 2)),
        )

        # Quocient sota la caixa del divisor
        q_digits = pas["quocient_digits"] if pas else []
        y_quocient = y_caixa_bottom + 10
        if q_digits:
            q_str = "".join(str(d) for d in q_digits)
            surf_q = self.font_xifra.render(q_str, True, self.VERD)
            self.pantalla.blit(
                surf_q,
                surf_q.get_rect(center=(x_caixa_esq + ample_caixa // 2, y_quocient + alt_fila // 2 - 2)),
            )

        # Files de càlcul / residu sota el dividend
        files = pas["files_calcul"] if pas else []
        for f_idx, fila in enumerate(files):
            y_f = y_dividend + (f_idx + 1) * (alt_fila - 4) + 6
            col_fi = fila["col_fi"]
            es_ultim = f_idx == len(files) - 1
            es_residu_final = fila["es_residu_final"]

            if es_residu_final:
                color_f = self.TARONJA if exercici["residu"] > 0 else self.VERD
            elif es_ultim:
                color_f = self.BLAU
            else:
                color_f = self.TEXT_SUAU

            surf_val = self.font_text_negreta.render(fila["text"], True, color_f)
            x_dret_alineat = centres_x[col_fi] + ample_col // 3
            self.pantalla.blit(surf_val, surf_val.get_rect(midright=(x_dret_alineat, y_f + 14)))

    def dibuixar_exercici(self, exercici, pas_actual):
        n_xifres = exercici["xifres_divisor"]
        titol_part = {
            1: "Divisions amb el divisor d'1 xifra",
            2: "Divisions amb el divisor de 2 xifres",
            3: "Divisions amb el divisor de 3 xifres",
        }[n_xifres]
        self._pintar_capcalera(titol_part)

        caixa = pygame.Rect(40, 86, self.amplada - 80, self.alcada - 176)
        pygame.draw.rect(self.pantalla, self.CAIXA, caixa, border_radius=16)
        pygame.draw.rect(self.pantalla, self.VORA, caixa, 2, border_radius=16)

        dividend = exercici["dividend"]
        divisor = exercici["divisor"]
        passos = exercici["passos"]
        total_passos = len(passos)
        completat = pas_actual >= total_passos

        etiqueta_tipus = "sense residu (exacta)" if exercici["es_exacta"] else "amb residu"
        pregunta = f"Divideix: {dividend} ÷ {divisor}  ({etiqueta_tipus})"
        surf_preg = self.font_mitjana.render(pregunta, True, self.TEXT)
        self.pantalla.blit(surf_preg, (caixa.x + 28, caixa.y + 18))

        estat_txt = f"Pas {pas_actual} de {total_passos}"
        surf_estat = self.font_text_negreta.render(estat_txt, True, self.VERD if completat else self.BLAU)
        self.pantalla.blit(surf_estat, surf_estat.get_rect(topright=(caixa.right - 28, caixa.y + 22)))

        y_linia = caixa.y + 68
        pygame.draw.line(self.pantalla, self.VORA, (caixa.x + 24, y_linia), (caixa.right - 24, y_linia), 2)

        # Zona esquerra: mètode de la caixa
        x_esq_caixa = caixa.x + 64
        self._dibuixar_caixa_divisio(exercici, pas_actual, x_esq_caixa, y_linia + 22)

        # Zona dreta: explicació pas a pas i prova de la divisió
        col_dreta_x = caixa.x + int(caixa.width * 0.46)
        ample_dreta = caixa.right - col_dreta_x - 32
        y_exp = y_linia + 22

        surf_tit_exp = self.font_mitjana.render("Explicació del pas:", True, self.BLAU)
        self.pantalla.blit(surf_tit_exp, (col_dreta_x, y_exp))
        y_exp += surf_tit_exp.get_height() + 12

        if pas_actual == 0:
            text_inici = (
                f"Posem el dividend ({dividend}) a l'esquerra i el divisor ({divisor}) dins la caixa. "
                f"Prem \"Següent pas\" per anar resolent la divisió i veure'n la prova al final."
            )
            self._renderitzar_text_ajustat(text_inici, self.font_text, self.TEXT_SUAU, col_dreta_x, y_exp, ample_dreta)
        else:
            pas = passos[pas_actual - 1]
            y_exp = self._renderitzar_text_ajustat(
                pas["explicacio"], self.font_text_negreta, self.TEXT, col_dreta_x, y_exp, ample_dreta
            )

            if pas["tipus"] == "divisio_pas":
                y_exp += 8
                resum = (
                    f"Quocient fins ara: {pas['quocient_parcial']}  |  "
                    f"Residu d'aquest pas: {pas['residu_pas']}"
                )
                self._renderitzar_text_ajustat(resum, self.font_text_negreta, self.TARONJA, col_dreta_x, y_exp, ample_dreta)

            elif pas["tipus"] == "prova_divisio" and pas["prova"]:
                pr = pas["prova"]
                y_exp += 10
                surf_tit_prova = self.font_mitjana.render("Prova de la divisió:", True, self.VERD)
                self.pantalla.blit(surf_tit_prova, (col_dreta_x, y_exp))
                y_exp += surf_tit_prova.get_height() + 8

                formula = f"Quocient × Divisor + Residu = Dividend"
                y_exp = self._renderitzar_text_ajustat(
                    formula, self.font_text_negreta, self.TEXT, col_dreta_x, y_exp, ample_dreta
                )

                calcul_prova = (
                    f"{pr['quocient']} × {pr['divisor']} + {pr['residu']} = "
                    f"{pr['producte_prova']} + {pr['residu']} = {pr['total_prova']}"
                )
                y_exp = self._renderitzar_text_ajustat(
                    calcul_prova, self.font_mitjana, self.BLAU, col_dreta_x, y_exp, ample_dreta
                )

                resum_final = (
                    f"Resultat final: Quocient = {pr['quocient']}"
                    + (f" i Residu = {pr['residu']}." if pr["residu"] > 0 else " (exacta, residu = 0).")
                )
                self._renderitzar_text_ajustat(
                    resum_final, self.font_text_negreta, self.VERD, col_dreta_x, y_exp + 4, ample_dreta
                )

        text_boto_pas = "Completat" if completat else "Següent pas"
        return self._dibuixar_peu_navegacio(
            te_enrere=True,
            botons_extra=[
                ("seguent_pas", text_boto_pas, self.VERD, self.VERD_HOVER),
                ("nou_exercici", "Nou exercici", self.BLAU, self.BLAU_HOVER),
            ],
        )

    def actualitzar(self):
        pygame.display.flip()
        self.rellotge.tick(60)