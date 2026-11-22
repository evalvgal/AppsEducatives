"""
Vista gràfica amb Pygame per a l'aplicació de Multiplicacions amb Portades.
Gestiona el menú de 3 parts (1, 2 i 3 xifres), la disposició vertical de la
multiplicació amb visualització gràfica de les portades i les explicacions
pas a pas acompanyant cada etapa.
"""
import pygame


class VistaMultiplicacio:
    def __init__(self):
        pygame.init()

        info = pygame.display.Info()
        self.amplada = info.current_w if info.current_w > 0 else 1280
        self.alcada = info.current_h if info.current_h > 0 else 800

        self.pantalla_completa = True
        self.pantalla = pygame.display.set_mode((self.amplada, self.alcada), pygame.FULLSCREEN)
        pygame.display.set_caption("Multiplicacions amb Portades - Educació Primària")

        self.rellotge = pygame.time.Clock()

        # Paleta educativa clara i contrastada
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
        m_xifra = int(36 * escala)

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
        self._pintar_capcalera("Multiplicacions amb Portades")

        cx = self.amplada // 2
        cy = self.alcada // 2
        w_boto = min(720, int(self.amplada * 0.72))
        h_boto = 88

        r_1 = pygame.Rect(cx - w_boto // 2, cy - 145, w_boto, h_boto)
        r_2 = pygame.Rect(cx - w_boto // 2, cy - 35, w_boto, h_boto)
        r_3 = pygame.Rect(cx - w_boto // 2, cy + 75, w_boto, h_boto)

        self._dibuixar_boto(r_1, "1. Multiplicacions amb portades d'1 xifra", self.BLAU, self.BLAU_HOVER)
        self._dibuixar_boto(r_2, "2. Multiplicacions amb portades de 2 xifres", self.VERD, self.VERD_HOVER)
        self._dibuixar_boto(r_3, "3. Multiplicacions amb portades de 3 xifres", self.TARONJA, self.TARONJA_HOVER)

        return {"xifra_1": r_1, "xifra_2": r_2, "xifra_3": r_3}

    def _x_columna(self, x_dreta_unitats, ample_col, col_idx):
        """
        Retorna la coordenada X central de la columna `col_idx` comptant des de la dreta:
        col_idx = 0 -> unitats, col_idx = 1 -> desenes, col_idx = 2 -> centenes, etc.
        """
        return x_dreta_unitats - col_idx * ample_col - ample_col // 2

    def _dibuixar_operacio_vertical(self, exercici, pas_actual, x_centre_zona, y_inici):
        """
        Dibuixa la multiplicació vertical pas a pas amb:
        - Línia superior de portades (per veure d'on surt la portada i amb què es suma)
        - Multiplicand (a dalt) i multiplicador (a baix, amb signe ×)
        - Productes parcials i suma final
        """
        x_val = exercici["x"]
        mult_val = exercici["multiplicador"]
        passos = exercici["passos"]
        n_files_mult = len(str(mult_val))

        pas = passos[pas_actual - 1] if pas_actual > 0 else None
        completat = pas_actual >= len(passos)

        str_x = str(x_val)
        str_m = str(mult_val)
        max_xifres = max(len(str_x), len(str_m), len(str(exercici["resultat_final"]))) + 1

        ample_col = 48
        alt_fila = 46
        x_dreta_unitats = x_centre_zona + (max_xifres * ample_col) // 2

        # 1. Zona de portades a dalt del multiplicand
        y_portades = y_inici
        portades_a_mostrar = []
        if pas:
            if pas["tipus"] in ("producte_xifra", "baixa_portada"):
                idx_f = pas["idx_fila"]
                p_sortida = pas["portades_sortida"][idx_f]
                # Mostrem les portades generades fins ara en aquesta fila
                for c_idx, p_val in enumerate(p_sortida):
                    if p_val > 0 and (pas["tipus"] == "baixa_portada" or c_idx <= pas["pos_x"]):
                        # La portada de la columna c_idx afecta la columna c_idx + 1
                        col_desti = c_idx + 1
                        es_entrant_ara = (
                            pas["tipus"] == "producte_xifra"
                            and pas["portada_entrant"] > 0
                            and col_desti == pas["pos_x"]
                        )
                        es_nova_ara = (
                            pas["tipus"] == "producte_xifra"
                            and p_val > 0
                            and col_desti == pas["pos_x"] + 1
                        )
                        portades_a_mostrar.append((col_desti, p_val, es_entrant_ara, es_nova_ara))
            elif pas["tipus"] == "suma_final":
                for c_idx, p_val in enumerate(pas["portades_suma"]):
                    if p_val > 0 and c_idx <= pas["pos_x"]:
                        col_desti = c_idx + 1
                        es_entrant_ara = pas["portada_entrant"] > 0 and col_desti == pas["pos_x"]
                        es_nova_ara = pas["portada_nova"] > 0 and col_desti == pas["pos_x"] + 1
                        portades_a_mostrar.append((col_desti, p_val, es_entrant_ara, es_nova_ara))

        for col_desti, p_val, es_entrant, es_nova in portades_a_mostrar:
            cx_p = self._x_columna(x_dreta_unitats, ample_col, col_desti)
            rect_p = pygame.Rect(cx_p - 15, y_portades, 30, 26)
            color_fons_p = (254, 243, 199) if (es_entrant or es_nova) else (241, 245, 249)
            color_vora_p = self.TARONJA if (es_entrant or es_nova) else self.VORA
            color_txt_p = self.TARONJA if (es_entrant or es_nova) else self.TEXT_SUAU

            pygame.draw.rect(self.pantalla, color_fons_p, rect_p, border_radius=6)
            pygame.draw.rect(self.pantalla, color_vora_p, rect_p, 2, border_radius=6)
            surf_p = self.font_petita.render(f"+{p_val}", True, color_txt_p)
            self.pantalla.blit(surf_p, surf_p.get_rect(center=rect_p.center))

        # 2. Fila del multiplicand (x)
        y_x = y_portades + 36
        digits_x_rev = list(reversed([int(c) for c in str_x]))
        for col_idx, dx in enumerate(digits_x_rev):
            cx = self._x_columna(x_dreta_unitats, ample_col, col_idx)
            es_actiu = (
                pas is not None
                and pas["tipus"] == "producte_xifra"
                and pas["pos_x"] == col_idx
            )
            if es_actiu:
                r_act = pygame.Rect(cx - ample_col // 2 + 4, y_x - 2, ample_col - 8, alt_fila - 4)
                pygame.draw.rect(self.pantalla, (219, 234, 254), r_act, border_radius=8)
                pygame.draw.rect(self.pantalla, self.BLAU, r_act, 2, border_radius=8)

            color_dx = self.BLAU if es_actiu else self.TEXT
            surf_dx = self.font_xifra.render(str(dx), True, color_dx)
            self.pantalla.blit(surf_dx, surf_dx.get_rect(center=(cx, y_x + alt_fila // 2 - 2)))

        # 3. Fila del multiplicador (y / yz / yzm) amb signe × a l'esquerra
        y_m = y_x + alt_fila + 2
        x_signe = self._x_columna(x_dreta_unitats, ample_col, max_xifres - 1) - 10
        surf_per = self.font_mitjana.render("×", True, self.TEXT)
        self.pantalla.blit(surf_per, surf_per.get_rect(center=(x_signe, y_m + alt_fila // 2 - 2)))

        digits_m_rev = list(reversed([int(c) for c in str_m]))
        for col_idx, dm in enumerate(digits_m_rev):
            cx = self._x_columna(x_dreta_unitats, ample_col, col_idx)
            es_actiu_m = (
                pas is not None
                and pas["tipus"] in ("producte_xifra", "baixa_portada")
                and pas["idx_fila"] == col_idx
            )
            if es_actiu_m:
                r_m = pygame.Rect(cx - ample_col // 2 + 4, y_m - 2, ample_col - 8, alt_fila - 4)
                pygame.draw.rect(self.pantalla, (243, 232, 255), r_m, border_radius=8)
                pygame.draw.rect(self.pantalla, self.LILA, r_m, 2, border_radius=8)

            color_dm = self.LILA if es_actiu_m else self.TEXT
            surf_dm = self.font_xifra.render(str(dm), True, color_dm)
            self.pantalla.blit(surf_dm, surf_dm.get_rect(center=(cx, y_m + alt_fila // 2 - 2)))

        # Ratlla horitzontal sota el multiplicador
        y_ratlla_1 = y_m + alt_fila + 4
        x_esq_ratlla = self._x_columna(x_dreta_unitats, ample_col, max_xifres - 1) - 24
        x_drt_ratlla = x_dreta_unitats + 6
        pygame.draw.line(self.pantalla, self.TEXT, (x_esq_ratlla, y_ratlla_1), (x_drt_ratlla, y_ratlla_1), 3)

        # 4. Productes parcials (si n_files_mult == 1, és directament la fila del resultat)
        y_parcials = y_ratlla_1 + 10
        files_visibles = pas["files_parcials"] if pas else [[] for _ in range(n_files_mult)]

        for idx_f in range(n_files_mult):
            y_f = y_parcials + idx_f * alt_fila
            digits_f = files_visibles[idx_f]

            # Marquem posicions reservades pel desplaçament de desenes/centenes amb un punt suau
            for desp in range(idx_f):
                cx_desp = self._x_columna(x_dreta_unitats, ample_col, desp)
                surf_dot = self.font_text_negreta.render("·", True, self.TEXT_SUAU)
                self.pantalla.blit(surf_dot, surf_dot.get_rect(center=(cx_desp, y_f + alt_fila // 2 - 2)))

            for pos_en_fila, d_val in enumerate(digits_f):
                col_real = idx_f + pos_en_fila
                cx = self._x_columna(x_dreta_unitats, ample_col, col_real)
                es_nou_digit = (
                    pas is not None
                    and pas["tipus"] in ("producte_xifra", "baixa_portada")
                    and pas["idx_fila"] == idx_f
                    and pos_en_fila == len(digits_f) - 1
                )
                color_d = self.VERD if es_nou_digit else self.TEXT
                surf_d = self.font_xifra.render(str(d_val), True, color_d)
                self.pantalla.blit(surf_d, surf_d.get_rect(center=(cx, y_f + alt_fila // 2 - 2)))

        # 5. Si hi ha més d'una fila, dibuixem ratlla de suma i fila de resultat final
        if n_files_mult > 1:
            y_ratlla_2 = y_parcials + n_files_mult * alt_fila + 6
            pygame.draw.line(self.pantalla, self.TEXT, (x_esq_ratlla, y_ratlla_2), (x_drt_ratlla, y_ratlla_2), 3)
            surf_mes = self.font_mitjana.render("+", True, self.TEXT)
            self.pantalla.blit(surf_mes, surf_mes.get_rect(center=(x_signe, y_ratlla_2 - alt_fila // 2)))

            y_suma = y_ratlla_2 + 10
            digits_suma = pas["suma_parcial_mostrada"] if (pas and pas["suma_parcial_mostrada"]) else []
            for col_idx, ds in enumerate(digits_suma):
                cx = self._x_columna(x_dreta_unitats, ample_col, col_idx)
                es_ultim_s = (
                    pas is not None
                    and pas["tipus"] == "suma_final"
                    and pas["pos_x"] == col_idx
                )
                color_ds = self.VERD if es_ultim_s else self.BLAU
                surf_ds = self.font_xifra.render(str(ds), True, color_ds)
                self.pantalla.blit(surf_ds, surf_ds.get_rect(center=(cx, y_suma + alt_fila // 2 - 2)))

        if completat:
            y_final_txt = (
                y_parcials + alt_fila + 18
                if n_files_mult == 1
                else y_parcials + n_files_mult * alt_fila + alt_fila + 24
            )
            surf_res = self.font_mitjana.render(
                f"Resultat: {x_val} × {mult_val} = {exercici['resultat_final']}",
                True,
                self.VERD,
            )
            self.pantalla.blit(surf_res, surf_res.get_rect(center=(x_centre_zona, y_final_txt)))

    def dibuixar_exercici(self, exercici, pas_actual):
        n_xifres = exercici["xifres_multiplicador"]
        titol_part = {
            1: "Multiplicacions amb portades (1 xifra)",
            2: "Multiplicacions amb portades (2 xifres)",
            3: "Multiplicacions amb portades (3 xifres)",
        }[n_xifres]
        self._pintar_capcalera(titol_part)

        caixa = pygame.Rect(40, 86, self.amplada - 80, self.alcada - 176)
        pygame.draw.rect(self.pantalla, self.CAIXA, caixa, border_radius=16)
        pygame.draw.rect(self.pantalla, self.VORA, caixa, 2, border_radius=16)

        x_val = exercici["x"]
        mult_val = exercici["multiplicador"]
        passos = exercici["passos"]
        total_passos = len(passos)
        completat = pas_actual >= total_passos

        pregunta = f"Calcula: {x_val} × {mult_val}"
        surf_preg = self.font_mitjana.render(pregunta, True, self.TEXT)
        self.pantalla.blit(surf_preg, (caixa.x + 28, caixa.y + 18))

        estat_txt = f"Pas {pas_actual} de {total_passos}"
        surf_estat = self.font_text_negreta.render(estat_txt, True, self.VERD if completat else self.BLAU)
        self.pantalla.blit(surf_estat, surf_estat.get_rect(topright=(caixa.right - 28, caixa.y + 22)))

        y_linia = caixa.y + 68
        pygame.draw.line(self.pantalla, self.VORA, (caixa.x + 24, y_linia), (caixa.right - 24, y_linia), 2)

        # Columna esquerra: operació vertical i portades
        col_esq_x = caixa.x + int(caixa.width * 0.24)
        self._dibuixar_operacio_vertical(exercici, pas_actual, col_esq_x, y_linia + 16)

        # Columna dreta: explicació gràfica i pas a pas
        col_dreta_x = caixa.x + int(caixa.width * 0.47)
        ample_dreta = caixa.right - col_dreta_x - 32
        y_exp = y_linia + 22

        surf_tit_exp = self.font_mitjana.render("Explicació del pas:", True, self.BLAU)
        self.pantalla.blit(surf_tit_exp, (col_dreta_x, y_exp))
        y_exp += surf_tit_exp.get_height() + 12

        if pas_actual == 0:
            text_inici = (
                f"Col·loquem el {x_val} a dalt i el {mult_val} a baix. "
                f"Prem \"Següent pas\" per començar a multiplicar de dreta a esquerra "
                f"i veure com es formen i se sumen les portades."
            )
            y_exp = self._renderitzar_text_ajustat(
                text_inici, self.font_text, self.TEXT_SUAU, col_dreta_x, y_exp, ample_dreta
            )
        else:
            pas = passos[pas_actual - 1]
            y_exp = self._renderitzar_text_ajustat(
                pas["explicacio"], self.font_text_negreta, self.TEXT, col_dreta_x, y_exp, ample_dreta
            )

            if pas["tipus"] == "producte_xifra":
                y_exp += 10
                resum_operacio = f"Operació: {pas['dx']} × {pas['dm']} = {pas['producte_base']}"
                if pas["portada_entrant"] > 0:
                    resum_operacio += f"  |  + portada ({pas['portada_entrant']}) = {pas['total']}"
                y_exp = self._renderitzar_text_ajustat(
                    resum_operacio, self.font_text_negreta, self.TARONJA, col_dreta_x, y_exp, ample_dreta
                )

                if pas["portada_nova"] > 0:
                    nota_portada = (
                        f"→ La xifra de les unitats ({pas['xifra_resultat']}) queda aquí i la portada "
                        f"({pas['portada_nova']}) passa a la columna següent per sumar-se al pròxim producte."
                    )
                else:
                    nota_portada = (
                        f"→ En aquest pas no hi ha portada nova (0). La xifra {pas['xifra_resultat']} es col·loca directament."
                    )
                y_exp = self._renderitzar_text_ajustat(
                    nota_portada, self.font_text, self.TEXT_SUAU, col_dreta_x, y_exp + 4, ample_dreta
                )

        if completat:
            y_exp += 14
            surf_fi = self.font_mitjana.render("Exercici completat!", True, self.VERD)
            self.pantalla.blit(surf_fi, (col_dreta_x, y_exp))
            y_exp += surf_fi.get_height() + 8
            self._renderitzar_text_ajustat(
                f"El resultat final de {x_val} × {mult_val} és {exercici['resultat_final']}. "
                "Pots prémer \"Nou exercici\" per practicar-ne un altre.",
                self.font_text,
                self.TEXT,
                col_dreta_x,
                y_exp,
                ample_dreta,
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