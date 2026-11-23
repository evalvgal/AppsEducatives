"""
Vista gràfica amb Pygame per a l'aplicació de Suma de Fraccions.
Mostra totes les fraccions amb format apilat, el càlcul pas a pas de l'm.c.m.
amb descomposició en ratlla vertical dels denominadors, la suma de fraccions,
la descomposició en ratlla vertical per trobar l'M.C.D. i les divisions pas a
pas pel M.C.D.
"""
import pygame


class VistaSumaFraccio:
    def __init__(self):
        pygame.init()

        info = pygame.display.Info()
        self.amplada = info.current_w if info.current_w > 0 else 1280
        self.alcada = info.current_h if info.current_h > 0 else 800

        self.pantalla_completa = True
        self.pantalla = pygame.display.set_mode((self.amplada, self.alcada), pygame.FULLSCREEN)
        pygame.display.set_caption("Suma de Fraccions i Reducció amb M.C.D. - Educació Primària")

        self.rellotge = pygame.time.Clock()

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
        escala = max(0.72, min(escala, 1.30))

        m_titol = int(38 * escala)
        m_mitjana = int(22 * escala)
        m_text = int(18 * escala)
        m_petita = int(15 * escala)
        m_fraccio = int(22 * escala)

        try:
            self.font_titol = pygame.font.SysFont("Arial", m_titol, bold=True)
            self.font_mitjana = pygame.font.SysFont("Arial", m_mitjana, bold=True)
            self.font_text = pygame.font.SysFont("Arial", m_text)
            self.font_text_negreta = pygame.font.SysFont("Arial", m_text, bold=True)
            self.font_petita = pygame.font.SysFont("Arial", m_petita, bold=True)
            self.font_fraccio = pygame.font.SysFont("Arial", m_fraccio, bold=True)
        except Exception:
            self.font_titol = pygame.font.Font(None, m_titol + 6)
            self.font_mitjana = pygame.font.Font(None, m_mitjana + 4)
            self.font_text = pygame.font.Font(None, m_text + 4)
            self.font_text_negreta = pygame.font.Font(None, m_text + 4)
            self.font_petita = pygame.font.Font(None, m_petita + 4)
            self.font_fraccio = pygame.font.Font(None, m_fraccio + 4)

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
            self.amplada = max(960, nova_amplada)
            self.alcada = max(700, nova_alcada)
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

    def _renderitzar_text_ajustat(self, text, font, color, x, y, max_ample, max_y=None, interlineat=4):
        """
        Renderitza text dividit en línies sense depassar `max_ample` ni `max_y` (si s'indica),
        i retorna la coordenada Y final.
        """
        paraules = text.split(" ")
        linia = []
        y_act = y
        pas_linia = font.get_linesize() + interlineat

        for paraula in paraules:
            prova = " ".join(linia + [paraula])
            if font.size(prova)[0] <= max_ample:
                linia.append(paraula)
            else:
                if max_y is not None and y_act + pas_linia > max_y:
                    return y_act
                if linia:
                    surf = font.render(" ".join(linia), True, color)
                    self.pantalla.blit(surf, (x, y_act))
                    y_act += pas_linia
                linia = [paraula]

        if linia:
            if max_y is None or y_act + pas_linia <= max_y:
                surf = font.render(" ".join(linia), True, color)
                self.pantalla.blit(surf, (x, y_act))
                y_act += pas_linia

        return y_act

    def _dibuixar_fraccio(self, num, den, cx, cy, color_num=None, color_den=None, color_ratlla=None, font=None):
        """
        Dibuixa una fracció amb el format apilat (numerador / ratlla / denominador)
        centrada horitzontalment en `cx` i verticalment en `cy`. Retorna l'amplada ocupada.
        """
        f_usada = font or self.font_fraccio
        c_n = color_num or self.TEXT
        c_d = color_den or self.TEXT
        c_r = color_ratlla or self.TEXT

        s_num = f_usada.render(str(num), True, c_n)
        s_den = f_usada.render(str(den), True, c_d)
        ample_ratlla = max(s_num.get_width(), s_den.get_width()) + 12

        y_ratlla = cy
        y_num = y_ratlla - 3 - s_num.get_height()
        y_den = y_ratlla + 3

        self.pantalla.blit(s_num, s_num.get_rect(centerx=cx, top=y_num))
        pygame.draw.line(self.pantalla, c_r, (cx - ample_ratlla // 2, y_ratlla), (cx + ample_ratlla // 2, y_ratlla), 2)
        self.pantalla.blit(s_den, s_den.get_rect(centerx=cx, top=y_den))

        return ample_ratlla

    def dibuixar_menu_principal(self):
        self._pintar_capcalera("Suma de Fraccions")

        cx = self.amplada // 2
        cy = self.alcada // 2
        w_boto = min(760, int(self.amplada * 0.76))
        h_boto = 96

        r_mateix = pygame.Rect(cx - w_boto // 2, cy - 85, w_boto, h_boto)
        r_diferent = pygame.Rect(cx - w_boto // 2, cy + 35, w_boto, h_boto)

        self._dibuixar_boto(
            r_mateix,
            "1. Sumes de fraccions amb el mateix denominador",
            self.BLAU,
            self.BLAU_HOVER,
        )
        self._dibuixar_boto(
            r_diferent,
            "2. Sumes de fraccions amb diferents denominadors",
            self.VERD,
            self.VERD_HOVER,
        )

        return {"mateix_den": r_mateix, "diferent_den": r_diferent}

    def _dibuixar_ratlla_descomposicio(self, files, x_esq, y_top, color_cap, max_y, alt_f=18):
        """
        Dibuixa la descomposició en factors primers amb ratlla vertical respectant `max_y`.
        Retorna la coordenada Y final.
        """
        if not files:
            return y_top

        x_ratlla = x_esq + 48
        y_act = y_top

        for fila in files:
            if y_act + alt_f > max_y:
                break
            es_ultim_nombre = fila["divisor"] is None
            s_nom = self.font_petita.render(
                str(fila["nombre"]),
                True,
                self.VERD if es_ultim_nombre else color_cap,
            )
            self.pantalla.blit(s_nom, s_nom.get_rect(right=x_ratlla - 7, centery=y_act + alt_f // 2))

            if fila["divisor"] is not None:
                s_div = self.font_petita.render(str(fila["divisor"]), True, self.LILA)
                self.pantalla.blit(s_div, (x_ratlla + 7, y_act + 1))

            y_act += alt_f

        if y_act > y_top:
            pygame.draw.line(self.pantalla, self.TEXT, (x_ratlla, y_top), (x_ratlla, y_act), 2)
        return y_act

    def _dibuixar_esquema_suma_grafic(self, pas, x_esq, y_top, ample_zona, max_y):
        """
        Dibuixa gràficament la suma de fraccions utilitzant sempre el format
        apilat per a totes les fraccions, i mostrant el càlcul pas a pas de l'm.c.m.
        amb ratlla vertical quan el denominador és diferent.
        """
        mateix = pas["mateix_denominador"]
        y_act = y_top + 26

        if mateix:
            a, b, den = pas["a"], pas["b"], pas["den"]
            te_resultat = pas["num_suma"] is not None

            if te_resultat:
                x1 = x_esq + int(ample_zona * 0.16)
                x_mes = x_esq + int(ample_zona * 0.31)
                x2 = x_esq + int(ample_zona * 0.46)
                x_eq = x_esq + int(ample_zona * 0.61)
                x_res = x_esq + int(ample_zona * 0.80)
            else:
                x1 = x_esq + int(ample_zona * 0.25)
                x_mes = x_esq + int(ample_zona * 0.50)
                x2 = x_esq + int(ample_zona * 0.75)

            self._dibuixar_fraccio(a, den, x1, y_act, color_num=self.BLAU, color_den=self.TEXT)
            s_mes = self.font_mitjana.render("+", True, self.TEXT)
            self.pantalla.blit(s_mes, s_mes.get_rect(center=(x_mes, y_act)))
            self._dibuixar_fraccio(b, den, x2, y_act, color_num=self.TARONJA, color_den=self.TEXT)

            if te_resultat and y_act + 36 <= max_y:
                s_eq = self.font_mitjana.render("=", True, self.TEXT)
                self.pantalla.blit(s_eq, s_eq.get_rect(center=(x_eq, y_act)))
                self._dibuixar_fraccio(
                    pas["num_suma"],
                    pas["den_suma"],
                    x_res,
                    y_act,
                    color_num=self.VERD,
                    color_den=self.VERD,
                    color_ratlla=self.VERD,
                )

            return y_act + 42

        # Denominadors diferents
        a, b, c, d = pas["a"], pas["b"], pas["c"], pas["d"]
        mcm = pas["mcm"]

        x1 = x_esq + int(ample_zona * 0.18)
        x_mes = x_esq + int(ample_zona * 0.34)
        x2 = x_esq + int(ample_zona * 0.50)

        self._dibuixar_fraccio(a, b, x1, y_act, color_num=self.BLAU, color_den=self.BLAU)
        s_mes = self.font_mitjana.render("+", True, self.TEXT)
        self.pantalla.blit(s_mes, s_mes.get_rect(center=(x_mes, y_act)))
        self._dibuixar_fraccio(c, d, x2, y_act, color_num=self.TARONJA, color_den=self.TARONJA)

        if mcm is not None:
            s_mcm = self.font_petita.render(f"m.c.m. = {mcm}", True, self.LILA)
            self.pantalla.blit(s_mcm, s_mcm.get_rect(center=(x_esq + int(ample_zona * 0.80), y_act)))

        y_actual = y_act + 44

        # Descomposició pas a pas dels denominadors b i d per calcular l'm.c.m.
        if (pas["desc_b_files"] or pas["desc_d_files"]) and y_actual + 34 <= max_y:
            x_col_b = x_esq + 18
            x_col_d = x_esq + ample_zona // 2 + 12

            s_lb = self.font_petita.render(f"Factors de {b}:", True, self.BLAU)
            s_ld = self.font_petita.render(f"Factors de {d}:", True, self.TARONJA)
            self.pantalla.blit(s_lb, (x_col_b, y_actual))
            self.pantalla.blit(s_ld, (x_col_d, y_actual))

            limit_desc = min(max_y - 24, y_actual + 128)
            yb = self._dibuixar_ratlla_descomposicio(pas["desc_b_files"], x_col_b, y_actual + 18, self.BLAU, limit_desc, alt_f=17)
            yd = self._dibuixar_ratlla_descomposicio(pas["desc_d_files"], x_col_d, y_actual + 18, self.TARONJA, limit_desc, alt_f=17)
            y_actual = max(yb, yd) + 4

            if pas["mcm_complet"] and mcm is not None and y_actual + 20 <= max_y:
                s_conc_mcm = self.font_petita.render(f"m.c.m.({b}, {d}) = {mcm}", True, self.LILA)
                self.pantalla.blit(s_conc_mcm, (x_esq + 18, y_actual))
                y_actual += 22

        # Fraccions equivalents a denominador m.c.m.
        if (pas["a_eq"] is not None or pas["c_eq"] is not None) and y_actual + 32 <= max_y:
            y_eq = y_actual + 16
            if pas["a_eq"] is not None:
                s_f1 = self.font_petita.render(f"×{pas['factor_a']} →", True, self.BLAU)
                self.pantalla.blit(s_f1, s_f1.get_rect(center=(x_esq + int(ample_zona * 0.14), y_eq)))
                self._dibuixar_fraccio(
                    pas["a_eq"],
                    mcm,
                    x_esq + int(ample_zona * 0.30),
                    y_eq,
                    color_num=self.BLAU,
                    color_den=self.BLAU,
                    color_ratlla=self.BLAU,
                    font=self.font_petita,
                )

            if pas["c_eq"] is not None:
                s_f2 = self.font_petita.render(f"×{pas['factor_c']} →", True, self.TARONJA)
                self.pantalla.blit(s_f2, s_f2.get_rect(center=(x_esq + int(ample_zona * 0.56), y_eq)))
                self._dibuixar_fraccio(
                    pas["c_eq"],
                    mcm,
                    x_esq + int(ample_zona * 0.74),
                    y_eq,
                    color_num=self.TARONJA,
                    color_den=self.TARONJA,
                    color_ratlla=self.TARONJA,
                    font=self.font_petita,
                )

            y_actual = y_eq + 32

        # Suma de les fraccions equivalents en format apilat
        if pas["num_suma"] is not None and y_actual + 34 <= max_y:
            y_sum = y_actual + 14
            s_sum_lbl = self.font_petita.render("Suma:", True, self.VERD)
            self.pantalla.blit(s_sum_lbl, (x_esq + 14, y_sum - 8))
            self._dibuixar_fraccio(
                pas["a_eq"],
                mcm,
                x_esq + int(ample_zona * 0.27),
                y_sum,
                color_num=self.BLAU,
                color_den=self.BLAU,
                color_ratlla=self.BLAU,
                font=self.font_petita,
            )
            s_m = self.font_text_negreta.render("+", True, self.TEXT)
            self.pantalla.blit(s_m, s_m.get_rect(center=(x_esq + int(ample_zona * 0.41), y_sum)))
            self._dibuixar_fraccio(
                pas["c_eq"],
                mcm,
                x_esq + int(ample_zona * 0.55),
                y_sum,
                color_num=self.TARONJA,
                color_den=self.TARONJA,
                color_ratlla=self.TARONJA,
                font=self.font_petita,
            )
            s_ig = self.font_text_negreta.render("=", True, self.TEXT)
            self.pantalla.blit(s_ig, s_ig.get_rect(center=(x_esq + int(ample_zona * 0.69), y_sum)))
            self._dibuixar_fraccio(
                pas["num_suma"],
                pas["den_suma"],
                x_esq + int(ample_zona * 0.84),
                y_sum,
                color_num=self.VERD,
                color_den=self.VERD,
                color_ratlla=self.VERD,
                font=self.font_petita,
            )
            return y_sum + 32

        return y_actual

    def _dibuixar_zona_reduccio_grafica(self, pas, x_esq, y_top, ample_zona, max_y):
        """
        Dibuixa 'Reducció de <numerador>/<denominador>' (amb format apilat),
        la descomposició en ratlla vertical per trobar l'M.C.D., les divisions pas a pas
        i la fracció reduïda final en format apilat.
        """
        num_r = pas["num_a_reduir"]
        den_r = pas["den_a_reduir"]
        if num_r is None or den_r is None or y_top + 36 > max_y:
            return

        pygame.draw.line(self.pantalla, self.VORA, (x_esq + 12, y_top), (x_esq + ample_zona - 12, y_top), 2)

        y_cap = y_top + 24
        s_lbl = self.font_mitjana.render("Reducció de", True, self.LILA)
        self.pantalla.blit(s_lbl, (x_esq + 16, y_cap - s_lbl.get_height() // 2))
        self._dibuixar_fraccio(
            num_r,
            den_r,
            x_esq + 16 + s_lbl.get_width() + 48,
            y_cap,
            color_num=self.LILA,
            color_den=self.LILA,
            color_ratlla=self.LILA,
            font=self.font_petita,
        )

        y_desc = y_cap + 28
        if y_desc + 20 <= max_y and (pas["desc_num_files"] or pas["desc_den_files"]):
            x_col_n = x_esq + 16
            x_col_d = x_esq + ample_zona // 2 + 10

            s_lbl_n = self.font_petita.render(f"Factors de {num_r}:", True, self.BLAU)
            s_lbl_d = self.font_petita.render(f"Factors de {den_r}:", True, self.TARONJA)
            self.pantalla.blit(s_lbl_n, (x_col_n, y_desc))
            self.pantalla.blit(s_lbl_d, (x_col_d, y_desc))

            reserva_inferior = 68 if pas["mcd"] is not None else 18
            limit_ratlla = max(y_desc + 22, max_y - reserva_inferior)

            y_f_n = self._dibuixar_ratlla_descomposicio(pas["desc_num_files"], x_col_n, y_desc + 18, self.BLAU, limit_ratlla, alt_f=17)
            y_f_d = self._dibuixar_ratlla_descomposicio(pas["desc_den_files"], x_col_d, y_desc + 18, self.TARONJA, limit_ratlla, alt_f=17)
            y_sota = max(y_f_n, y_f_d) + 6
        else:
            y_sota = y_desc

        if pas["mcd"] is not None and y_sota + 18 <= max_y:
            s_mcd = self.font_text_negreta.render(f"M.C.D.({num_r}, {den_r}) = {pas['mcd']}", True, self.LILA)
            self.pantalla.blit(s_mcd, (x_esq + 16, y_sota))
            y_sota += 20

        if pas["div_num_fet"] and pas["num_reduit"] is not None and y_sota + 18 <= max_y:
            s_dn = self.font_petita.render(
                f"Num.: {num_r} ÷ {pas['mcd']} = {pas['num_reduit']}",
                True,
                self.BLAU,
            )
            self.pantalla.blit(s_dn, (x_esq + 22, y_sota))
            y_sota += 18

        if pas["div_den_fet"] and pas["den_reduit"] is not None and y_sota + 24 <= max_y:
            s_dd = self.font_petita.render(
                f"Den.: {den_r} ÷ {pas['mcd']} = {pas['den_reduit']}",
                True,
                self.TARONJA,
            )
            self.pantalla.blit(s_dd, (x_esq + 22, y_sota))

            self._dibuixar_fraccio(
                pas["num_reduit"],
                pas["den_reduit"],
                x_esq + ample_zona - 48,
                y_sota + 10,
                color_num=self.VERD,
                color_den=self.VERD,
                color_ratlla=self.VERD,
                font=self.font_petita,
            )

    def dibuixar_exercici(self, exercici, pas_actual):
        mateix = exercici["mateix_denominador"]
        titol = (
            "1. Sumes de fraccions amb el mateix denominador"
            if mateix
            else "2. Sumes de fraccions amb diferents denominadors"
        )
        self._pintar_capcalera(titol)

        caixa = pygame.Rect(40, 86, self.amplada - 80, self.alcada - 176)
        pygame.draw.rect(self.pantalla, self.CAIXA, caixa, border_radius=16)
        pygame.draw.rect(self.pantalla, self.VORA, caixa, 2, border_radius=16)

        passos = exercici["passos"]
        total_passos = len(passos)
        completat = pas_actual >= total_passos

        if mateix:
            enunciat = f"Suma: {exercici['a']}/{exercici['den']} + {exercici['b']}/{exercici['den']}"
        else:
            enunciat = f"Suma: {exercici['a']}/{exercici['b']} + {exercici['c']}/{exercici['d']}"

        surf_enun = self.font_mitjana.render(enunciat, True, self.TEXT)
        self.pantalla.blit(surf_enun, (caixa.x + 28, caixa.y + 18))

        estat_txt = f"Pas {pas_actual} de {total_passos}"
        surf_estat = self.font_text_negreta.render(estat_txt, True, self.VERD if completat else self.BLAU)
        self.pantalla.blit(surf_estat, surf_estat.get_rect(topright=(caixa.right - 28, caixa.y + 22)))

        y_linia = caixa.y + 64
        pygame.draw.line(self.pantalla, self.VORA, (caixa.x + 24, y_linia), (caixa.right - 24, y_linia), 2)

        max_y_contingut = caixa.bottom - 14
        ample_esq = int(caixa.width * 0.50)
        x_esq = caixa.x + 16

        if pas_actual == 0:
            pas_inicial = {
                "mateix_denominador": mateix,
                "a": exercici["a"],
                "b": exercici["b"],
                "c": exercici["c"],
                "d": exercici["d"],
                "den": exercici["den"],
                "mcm": None,
                "mcm_complet": False,
                "desc_b_files": [],
                "desc_d_files": [],
                "factor_a": None,
                "factor_c": None,
                "a_eq": None,
                "c_eq": None,
                "num_suma": None,
                "den_suma": None,
                "num_a_reduir": None,
                "den_a_reduir": None,
                "desc_num_files": [],
                "desc_den_files": [],
                "mcd": None,
                "div_num_fet": False,
                "div_den_fet": False,
                "num_reduit": None,
                "den_reduit": None,
            }
            self._dibuixar_esquema_suma_grafic(pas_inicial, x_esq, y_linia + 8, ample_esq, max_y_contingut)
            pas = None
        else:
            pas = passos[pas_actual - 1]
            # Si estem en els passos inicials de càlcul de l'm.c.m., reservem més alçada per a la descomposició
            mostra_reduccio = pas["num_a_reduir"] is not None
            limit_suma = (max_y_contingut - 185) if mostra_reduccio else max_y_contingut
            y_despres = self._dibuixar_esquema_suma_grafic(pas, x_esq, y_linia + 8, ample_esq, limit_suma)
            if mostra_reduccio:
                self._dibuixar_zona_reduccio_grafica(pas, x_esq, y_despres + 6, ample_esq, max_y_contingut)

        x_sep = caixa.x + ample_esq + 24
        pygame.draw.line(self.pantalla, self.VORA, (x_sep, y_linia + 14), (x_sep, caixa.bottom - 14), 2)

        col_dreta_x = x_sep + 22
        ample_dreta = caixa.right - col_dreta_x - 24
        y_exp = y_linia + 16

        if pas is None:
            y_exp = self._renderitzar_text_ajustat(
                "Explicació pas a pas:",
                self.font_mitjana,
                self.BLAU,
                col_dreta_x,
                y_exp,
                ample_dreta,
                max_y=max_y_contingut,
            )
            y_exp += 6

            text_inici = (
                "Prem \"Següent pas\" per veure gràficament com es fa la suma, "
                "la descomposició en ratlla vertical per trobar l'm.c.m. i l'M.C.D., "
                "i la divisió pas a pas per reduir la fracció."
            )
            self._renderitzar_text_ajustat(
                text_inici,
                self.font_text,
                self.TEXT_SUAU,
                col_dreta_x,
                y_exp,
                ample_dreta,
                max_y=max_y_contingut,
            )
        else:
            y_exp = self._renderitzar_text_ajustat(
                pas["titol_pas"],
                self.font_mitjana,
                self.BLAU,
                col_dreta_x,
                y_exp,
                ample_dreta,
                max_y=max_y_contingut,
            )
            y_exp += 8

            y_exp = self._renderitzar_text_ajustat(
                pas["explicacio"],
                self.font_text_negreta,
                self.TEXT,
                col_dreta_x,
                y_exp,
                ample_dreta,
                max_y=max_y_contingut - 44,
                interlineat=5,
            )

            if completat and y_exp + 34 <= max_y_contingut:
                y_exp += 10
                res_final = f"Resultat final reduït: {exercici['num_reduit']}/{exercici['den_reduit']}"
                self._renderitzar_text_ajustat(
                    res_final,
                    self.font_mitjana,
                    self.VERD,
                    col_dreta_x,
                    y_exp,
                    ample_dreta,
                    max_y=max_y_contingut,
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