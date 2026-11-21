"""
Vista gràfica amb Pygame per a l'aplicació de Mínim Comú Múltiple (m.c.m.)
i Màxim Comú Divisor (M.C.D.).
Gestiona la detecció de resolució a pantalla completa, la renderització de les
pantalles de menú, les dues pàgines de teoria amb factorització en ratlla vertical
i la pantalla d'exercicis resolts pas a pas.
"""
import pygame


class VistaMcmMcd:
    def __init__(self):
        pygame.init()

        # Detecció automàtica de la resolució nativa (PC, Mac o Pissarra Digital)
        info = pygame.display.Info()
        self.amplada = info.current_w if info.current_w > 0 else 1280
        self.alcada = info.current_h if info.current_h > 0 else 800

        self.pantalla_completa = True
        self.pantalla = pygame.display.set_mode((self.amplada, self.alcada), pygame.FULLSCREEN)
        pygame.display.set_caption("Mínim Comú Múltiple i Màxim Comú Divisor - Primària")

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
        m_petita = int(17 * escala)

        try:
            self.font_titol = pygame.font.SysFont("Arial", m_titol, bold=True)
            self.font_mitjana = pygame.font.SysFont("Arial", m_mitjana, bold=True)
            self.font_text = pygame.font.SysFont("Arial", m_text)
            self.font_text_negreta = pygame.font.SysFont("Arial", m_text, bold=True)
            self.font_petita = pygame.font.SysFont("Arial", m_petita, bold=True)
        except Exception:
            self.font_titol = pygame.font.Font(None, m_titol + 6)
            self.font_mitjana = pygame.font.Font(None, m_mitjana + 4)
            self.font_text = pygame.font.Font(None, m_text + 4)
            self.font_text_negreta = pygame.font.Font(None, m_text + 4)
            self.font_petita = pygame.font.Font(None, m_petita + 4)

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

    def _dibuixar_expressio_amb_exponents(self, termes, font_base, color, x, y, prefix="", sufix=""):
        """
        Dibuixa expressions amb potències renderitzant cada exponent amb una font
        més petita i elevada a dalt a la dreta de la base.
        Retorna la coordenada Y de la línia següent.
        """
        font_exp = self.font_petita
        x_act = x

        if prefix:
            surf_pref = font_base.render(prefix, True, color)
            self.pantalla.blit(surf_pref, (x_act, y))
            x_act += surf_pref.get_width()

        if not termes:
            surf_u = font_base.render("1", True, color)
            self.pantalla.blit(surf_u, (x_act, y))
            x_act += surf_u.get_width()
        else:
            for idx, (base_str, exp_str) in enumerate(termes):
                if idx > 0:
                    surf_sep = font_base.render(" · ", True, color)
                    self.pantalla.blit(surf_sep, (x_act, y))
                    x_act += surf_sep.get_width()

                surf_base = font_base.render(base_str, True, color)
                self.pantalla.blit(surf_base, (x_act, y))
                x_act += surf_base.get_width()

                if exp_str:
                    surf_exp = font_exp.render(exp_str, True, color)
                    y_exp = y - max(2, surf_exp.get_height() // 4)
                    self.pantalla.blit(surf_exp, (x_act + 1, y_exp))
                    x_act += surf_exp.get_width() + 2

        if sufix:
            surf_suf = font_base.render(sufix, True, color)
            self.pantalla.blit(surf_suf, (x_act, y))

        return y + font_base.get_linesize() + 6

    def _dibuixar_taula_descomposicio(self, numero, passos_visibles, x_centre, y_inici, alcada_maxima, pas_actiu_index=None):
        """
        Dibuixa la descomposició clàssica amb ratlla vertical:
        Columna esquerra: dividends / quocients
        Ratlla vertical central
        Columna dreta: factors primers
        """
        ample_col = 85
        alt_fila = 32
        files_necessaries = len(passos_visibles) + 1
        alcada_necessaria = files_necessaries * alt_fila + 8

        if alcada_necessaria > alcada_maxima and files_necessaries > 0:
            alt_fila = max(22, (alcada_maxima - 8) // files_necessaries)

        x_esquerra = x_centre - ample_col
        x_dreta = x_centre + 14
        y_top = y_inici
        y_bottom = y_top + files_necessaries * alt_fila

        # Fons ressaltat del pas actiu (dibuixat abans dels textos)
        if pas_actiu_index is not None and 0 <= pas_actiu_index < len(passos_visibles):
            y_fila_act = y_top + pas_actiu_index * alt_fila
            resaltat = pygame.Rect(x_esquerra - 8, y_fila_act + 2, ample_col * 2 + 16, alt_fila - 4)
            pygame.draw.rect(self.pantalla, (232, 248, 245), resaltat, border_radius=6)

        # Ratlla vertical central
        pygame.draw.line(self.pantalla, self.TEXT, (x_centre, y_top), (x_centre, y_bottom), 3)

        # Columna esquerra: nombre inicial i quocients obtinguts
        valors_esquerra = [numero] + [pas[2] for pas in passos_visibles]
        for fila_idx, val in enumerate(valors_esquerra):
            y_centre_fila = y_top + fila_idx * alt_fila + alt_fila // 2
            es_quocient_ultim_pas = pas_actiu_index is not None and fila_idx == pas_actiu_index + 1
            color_esq = self.BLAU if es_quocient_ultim_pas else self.TEXT
            surf_esq = self.font_text_negreta.render(str(val), True, color_esq)
            self.pantalla.blit(surf_esq, surf_esq.get_rect(midright=(x_centre - 14, y_centre_fila)))

        # Columna dreta: factors primers en cada pas
        for idx, (_, divisor, _) in enumerate(passos_visibles):
            y_centre_fila = y_top + idx * alt_fila + alt_fila // 2
            es_ultim_pas = pas_actiu_index is not None and idx == pas_actiu_index
            color_factor = self.VERD if es_ultim_pas else self.LILA
            surf_div = self.font_text_negreta.render(str(divisor), True, color_factor)
            self.pantalla.blit(surf_div, surf_div.get_rect(midleft=(x_dreta, y_centre_fila)))

        return y_bottom

    def dibuixar_menu_principal(self):
        self._pintar_capcalera("Mínim Comú Múltiple i Màxim Comú Divisor")

        cx = self.amplada // 2
        cy = self.alcada // 2
        w_boto = min(680, int(self.amplada * 0.68))
        h_boto = 105

        r_teoria = pygame.Rect(cx - w_boto // 2, cy - 115, w_boto, h_boto)
        r_exercicis = pygame.Rect(cx - w_boto // 2, cy + 25, w_boto, h_boto)

        self._dibuixar_boto(r_teoria, "1. Teoria (m.c.m. i M.C.D. amb exemples)", self.BLAU, self.BLAU_HOVER)
        self._dibuixar_boto(r_exercicis, "2. Exercicis resolts pas a pas", self.VERD, self.VERD_HOVER)

        return {"teoria": r_teoria, "exercicis": r_exercicis}

    def _dibuixar_pagina_teoria_comuna(self, dades, num_pagina, es_mcm):
        self._pintar_capcalera(f"Teoria — Pàgina {num_pagina} de 2: {dades['titol']}")

        caixa = pygame.Rect(40, 86, self.amplada - 80, self.alcada - 176)
        pygame.draw.rect(self.pantalla, self.CAIXA, caixa, border_radius=16)
        pygame.draw.rect(self.pantalla, self.VORA, caixa, 2, border_radius=16)

        y_act = self._renderitzar_text_ajustat(
            dades["definicio"],
            self.font_text,
            self.TEXT,
            caixa.x + 28,
            caixa.y + 20,
            caixa.width - 56,
            interlineat=4,
        )

        y_div = y_act + 10
        pygame.draw.line(self.pantalla, self.VORA, (caixa.x + 24, y_div), (caixa.right - 24, y_div), 2)

        ex = dades["exemple"]
        x_val, y_val = ex["x"], ex["y"]

        y_contingut = y_div + 14
        alcada_taula = caixa.bottom - y_contingut - 44

        col1_x = caixa.x + int(caixa.width * 0.14)
        col2_x = caixa.x + int(caixa.width * 0.34)
        col3_x = caixa.x + int(caixa.width * 0.47)
        ample_col3 = caixa.right - col3_x - 28

        t1 = self.font_text_negreta.render(f"Descomposició de {x_val}", True, self.BLAU)
        self.pantalla.blit(t1, t1.get_rect(center=(col1_x, y_contingut + 12)))
        self._dibuixar_taula_descomposicio(
            x_val,
            ex["passos_x"],
            x_centre=col1_x,
            y_inici=y_contingut + 36,
            alcada_maxima=alcada_taula,
        )

        t2 = self.font_text_negreta.render(f"Descomposició de {y_val}", True, self.BLAU)
        self.pantalla.blit(t2, t2.get_rect(center=(col2_x, y_contingut + 12)))
        self._dibuixar_taula_descomposicio(
            y_val,
            ex["passos_y"],
            x_centre=col2_x,
            y_inici=y_contingut + 36,
            alcada_maxima=alcada_taula,
        )

        tit_ex = f"Exemple: calcular el {'m.c.m.' if es_mcm else 'M.C.D.'}({x_val}, {y_val})"
        surf_tit_ex = self.font_mitjana.render(tit_ex, True, self.TARONJA if es_mcm else self.VERD)
        self.pantalla.blit(surf_tit_ex, (col3_x, y_contingut + 6))

        y_r = y_contingut + 48
        y_r = self._renderitzar_text_ajustat(
            "1. Expressió en factors primers:",
            self.font_text_negreta,
            self.TEXT,
            col3_x,
            y_r,
            ample_col3,
        )
        y_r = self._dibuixar_expressio_amb_exponents(
            ex["termes_x"],
            self.font_text_negreta,
            self.LILA,
            col3_x + 12,
            y_r,
            prefix=f"• {x_val} = ",
        )
        y_r = self._dibuixar_expressio_amb_exponents(
            ex["termes_y"],
            self.font_text_negreta,
            self.LILA,
            col3_x + 12,
            y_r,
            prefix=f"• {y_val} = ",
        )

        y_r += 10
        if es_mcm:
            regla = "2. Prenem els factors comuns i no comuns amb el MAJOR exponent:"
            y_r = self._renderitzar_text_ajustat(regla, self.font_text_negreta, self.TEXT, col3_x, y_r, ample_col3)
            self._dibuixar_expressio_amb_exponents(
                ex["termes_mcm"],
                self.font_mitjana,
                self.BLAU,
                col3_x,
                y_r + 6,
                prefix=f"m.c.m.({x_val}, {y_val}) = ",
                sufix=f" = {ex['mcm_valor']}",
            )
        else:
            regla = "2. Prenem només els factors comuns amb el MENOR exponent:"
            y_r = self._renderitzar_text_ajustat(regla, self.font_text_negreta, self.TEXT, col3_x, y_r, ample_col3)
            if ex["te_comuns"]:
                self._dibuixar_expressio_amb_exponents(
                    ex["termes_mcd"],
                    self.font_mitjana,
                    self.VERD,
                    col3_x,
                    y_r + 6,
                    prefix=f"M.C.D.({x_val}, {y_val}) = ",
                    sufix=f" = {ex['mcd_valor']}",
                )
            else:
                self._renderitzar_text_ajustat(
                    f"M.C.D.({x_val}, {y_val}) = 1 (no hi ha factors comuns)",
                    self.font_mitjana,
                    self.VERD,
                    col3_x,
                    y_r + 6,
                    ample_col3,
                )

    def dibuixar_teoria_pagina_1(self, dades):
        self._dibuixar_pagina_teoria_comuna(dades, num_pagina=1, es_mcm=True)
        return self._dibuixar_peu_navegacio(
            te_enrere=True,
            botons_extra=[("pagina_2", "Pàgina 2: M.C.D. →", self.TARONJA, self.TARONJA_HOVER)],
        )

    def dibuixar_teoria_pagina_2(self, dades):
        self._dibuixar_pagina_teoria_comuna(dades, num_pagina=2, es_mcm=False)
        return self._dibuixar_peu_navegacio(
            te_enrere=True,
            botons_extra=[("pagina_1", "← Pàgina 1: m.c.m.", self.BLAU, self.BLAU_HOVER)],
        )

    def dibuixar_exercicis(self, exercici, etapa_actual):
        self._pintar_capcalera("Exercicis resolts: m.c.m. i M.C.D.")

        caixa = pygame.Rect(40, 86, self.amplada - 80, self.alcada - 176)
        pygame.draw.rect(self.pantalla, self.CAIXA, caixa, border_radius=16)
        pygame.draw.rect(self.pantalla, self.VORA, caixa, 2, border_radius=16)

        x_val = exercici["x"]
        y_val = exercici["y"]
        passos_x = exercici["passos_x"]
        passos_y = exercici["passos_y"]

        nx = len(passos_x)
        ny = len(passos_y)
        total_etapes = nx + ny + 2
        completat = etapa_actual >= total_etapes

        pregunta = f"Quin és el mínim comú múltiple i màxim comú divisor entre {x_val} i {y_val}?"
        self._renderitzar_text_ajustat(pregunta, self.font_mitjana, self.TEXT, caixa.x + 28, caixa.y + 18, caixa.width - 210)

        estat_txt = f"Pas {etapa_actual} de {total_etapes}"
        surf_pas = self.font_text_negreta.render(estat_txt, True, self.VERD if completat else self.BLAU)
        self.pantalla.blit(surf_pas, surf_pas.get_rect(topright=(caixa.right - 28, caixa.y + 22)))

        y_linia = caixa.y + 72
        pygame.draw.line(self.pantalla, self.VORA, (caixa.x + 24, y_linia), (caixa.right - 24, y_linia), 2)

        mostrats_x = min(etapa_actual, nx)
        mostrats_y = max(0, min(etapa_actual - nx, ny))

        pas_actiu_x = mostrats_x - 1 if 1 <= etapa_actual <= nx else None
        pas_actiu_y = mostrats_y - 1 if nx < etapa_actual <= nx + ny else None

        y_contingut = y_linia + 14
        alcada_taula = caixa.bottom - y_contingut - 44

        col1_x = caixa.x + int(caixa.width * 0.13)
        col2_x = caixa.x + int(caixa.width * 0.33)
        col3_x = caixa.x + int(caixa.width * 0.46)
        ample_col3 = caixa.right - col3_x - 28

        t1 = self.font_text_negreta.render(f"Nombre {x_val}", True, self.BLAU)
        self.pantalla.blit(t1, t1.get_rect(center=(col1_x, y_contingut + 12)))
        self._dibuixar_taula_descomposicio(
            x_val,
            passos_x[:mostrats_x],
            x_centre=col1_x,
            y_inici=y_contingut + 36,
            alcada_maxima=alcada_taula,
            pas_actiu_index=pas_actiu_x,
        )

        t2 = self.font_text_negreta.render(f"Nombre {y_val}", True, self.BLAU)
        self.pantalla.blit(t2, t2.get_rect(center=(col2_x, y_contingut + 12)))
        self._dibuixar_taula_descomposicio(
            y_val,
            passos_y[:mostrats_y],
            x_centre=col2_x,
            y_inici=y_contingut + 36,
            alcada_maxima=alcada_taula,
            pas_actiu_index=pas_actiu_y,
        )

        y_r = y_contingut + 8
        if etapa_actual == 0:
            indicacio = (
                f"Prem el botó \"Següent pas\" per anar descomposant primer el {x_val}, "
                f"després el {y_val}, i finalment calcular el m.c.m. i el M.C.D."
            )
            self._renderitzar_text_ajustat(indicacio, self.font_text, self.TEXT_SUAU, col3_x, y_r, ample_col3)

        elif etapa_actual <= nx:
            divid, divis, quoc = passos_x[mostrats_x - 1]
            msg = f"Descomposant {x_val}: dividim {divid} entre {divis} i obtenim {quoc}."
            self._renderitzar_text_ajustat(msg, self.font_text_negreta, self.TEXT, col3_x, y_r, ample_col3)

        elif etapa_actual <= nx + ny:
            divid, divis, quoc = passos_y[mostrats_y - 1]
            msg = f"Descomposant {y_val}: dividim {divid} entre {divis} i obtenim {quoc}."
            self._renderitzar_text_ajustat(msg, self.font_text_negreta, self.TEXT, col3_x, y_r, ample_col3)

        if etapa_actual >= nx + ny + 1:
            y_r = y_contingut + 44 if etapa_actual == nx + ny + 1 else y_contingut + 8
            surf_f = self.font_text_negreta.render("Descomposició en factors primers:", True, self.TEXT)
            self.pantalla.blit(surf_f, (col3_x, y_r))
            y_r += surf_f.get_height() + 6

            y_r = self._dibuixar_expressio_amb_exponents(
                exercici["termes_x"],
                self.font_text_negreta,
                self.LILA,
                col3_x,
                y_r,
                prefix=f"• {x_val} = ",
            )
            y_r = self._dibuixar_expressio_amb_exponents(
                exercici["termes_y"],
                self.font_text_negreta,
                self.LILA,
                col3_x,
                y_r,
                prefix=f"• {y_val} = ",
            )

        if etapa_actual >= total_etapes:
            y_r += 12
            if exercici["termes_mcm"]:
                y_r = self._dibuixar_expressio_amb_exponents(
                    exercici["termes_mcm"],
                    self.font_mitjana,
                    self.BLAU,
                    col3_x,
                    y_r,
                    prefix=f"m.c.m. ({x_val}, {y_val}) = ",
                    sufix=f" = {exercici['mcm_valor']}",
                )
            else:
                mcm_txt = f"m.c.m. ({x_val}, {y_val}) = {exercici['mcm_valor']}"
                y_r = self._renderitzar_text_ajustat(mcm_txt, self.font_mitjana, self.BLAU, col3_x, y_r, ample_col3)

            if exercici["te_comuns"]:
                self._dibuixar_expressio_amb_exponents(
                    exercici["termes_mcd"],
                    self.font_mitjana,
                    self.VERD,
                    col3_x,
                    y_r + 6,
                    prefix=f"M.C.D. ({x_val}, {y_val}) = ",
                    sufix=f" = {exercici['mcd_valor']}",
                )
            else:
                mcd_txt = f"M.C.D. ({x_val}, {y_val}) = 1"
                self._renderitzar_text_ajustat(mcd_txt, self.font_mitjana, self.VERD, col3_x, y_r + 6, ample_col3)

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