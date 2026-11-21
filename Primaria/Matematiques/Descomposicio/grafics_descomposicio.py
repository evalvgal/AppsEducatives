# -*- coding: utf-8 -*-
import pygame


class VistaDescomposicio:
    def __init__(self):
        pygame.init()

        # Detecció automàtica de la resolució nativa (PC, Mac o Pissarra Digital)
        info = pygame.display.Info()
        self.amplada = info.current_w if info.current_w > 0 else 1280
        self.alcada = info.current_h if info.current_h > 0 else 800

        self.pantalla_completa = True
        self.pantalla = pygame.display.set_mode((self.amplada, self.alcada), pygame.FULLSCREEN)
        pygame.display.set_caption("Descomposició en Factors Primers - Primària")

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

        m_titol = int(44 * escala)
        m_mitjana = int(28 * escala)
        m_text = int(21 * escala)
        m_petita = int(17 * escala)
        m_gran = int(56 * escala)

        try:
            self.font_titol = pygame.font.SysFont("Arial", m_titol, bold=True)
            self.font_mitjana = pygame.font.SysFont("Arial", m_mitjana, bold=True)
            self.font_text = pygame.font.SysFont("Arial", m_text)
            self.font_text_negreta = pygame.font.SysFont("Arial", m_text, bold=True)
            self.font_petita = pygame.font.SysFont("Arial", m_petita)
            self.font_gran = pygame.font.SysFont("Arial", m_gran, bold=True)
        except Exception:
            self.font_titol = pygame.font.Font(None, m_titol + 6)
            self.font_mitjana = pygame.font.Font(None, m_mitjana + 4)
            self.font_text = pygame.font.Font(None, m_text + 4)
            self.font_text_negreta = pygame.font.Font(None, m_text + 4)
            self.font_petita = pygame.font.Font(None, m_petita + 4)
            self.font_gran = pygame.font.Font(None, m_gran + 8)

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
            self.amplada = max(900, nova_amplada)
            self.alcada = max(650, nova_alcada)
            self.pantalla = pygame.display.set_mode((self.amplada, self.alcada), pygame.RESIZABLE)
            self._carregar_fonts()

    def obtenir_rect_sortir(self):
        return pygame.Rect(self.amplada - 150, 22, 125, 48)

    def _dibuixar_boto(self, rect, text, color_base, color_hover, font=None, color_text=None, actiu=True):
        font_usada = font or self.font_mitjana
        color_txt = color_text or self.BLANC
        pos_ratoli = pygame.mouse.get_pos()

        if not actiu:
            pygame.draw.rect(self.pantalla, (226, 232, 240), rect, border_radius=14)
            surf = font_usada.render(text, True, (148, 163, 184))
            self.pantalla.blit(surf, surf.get_rect(center=rect.center))
            return rect

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
        """
        Dibuixa la barra inferior i retorna un diccionari amb els rectangles clicables.
        `botons_extra` és una llista de tuples: (clau, text, color_base, color_hover)
        """
        rects = {}
        y_peu = self.alcada - 76

        if te_enrere:
            r_enrere = pygame.Rect(40, y_peu, 220, 52)
            self._dibuixar_boto(r_enrere, text_enrere, self.GRIS_BOTO, self.GRIS_HOVER, font=self.font_text_negreta, color_text=self.TEXT)
            rects["enrere"] = r_enrere

        if botons_extra:
            ample_b = 230
            espai = 20
            total = len(botons_extra) * ample_b + (len(botons_extra) - 1) * espai
            x_actual = self.amplada - 25 - total
            for clau, text, c_base, c_hover in botons_extra:
                r_b = pygame.Rect(x_actual, y_peu, ample_b, 52)
                self._dibuixar_boto(r_b, text, c_base, c_hover, font=self.font_text_negreta)
                rects[clau] = r_b
                x_actual += ample_b + espai

        return rects

    def _renderitzar_text_ajustat(self, text, font, color, x, y, max_ample, interlineat=6):
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

    def _dibuixar_taula_descomposicio(self, numero, passos_visibles, x_centre, y_inici, alcada_maxima, pas_actiu_index=None):
        """
        Dibuixa la descomposició clàssica amb la ratlla vertical:
        Columna esquerra: dividends / quocients (acaba en 1)
        Ratlla vertical central
        Columna dreta: factors primers
        """
        ample_col = 110
        alt_fila = 34
        files_necessaries = len(passos_visibles) + 1
        alcada_necessaria = files_necessaries * alt_fila + 10

        if alcada_necessaria > alcada_maxima and files_necessaries > 0:
            alt_fila = max(24, (alcada_maxima - 10) // files_necessaries)

        x_esquerra = x_centre - ample_col
        x_dreta = x_centre + 18
        y_top = y_inici
        y_bottom = y_top + files_necessaries * alt_fila

        # Ratlla vertical central
        pygame.draw.line(self.pantalla, self.TEXT, (x_centre, y_top), (x_centre, y_bottom), 3)

        # Primera fila: nombre inicial
        surf_num = self.font_text_negreta.render(str(numero), True, self.TEXT)
        self.pantalla.blit(surf_num, surf_num.get_rect(midright=(x_centre - 18, y_top + alt_fila // 2)))

        for idx, (_, divisor, nou_quocient) in enumerate(passos_visibles):
            y_fila = y_top + idx * alt_fila
            y_centre_fila = y_fila + alt_fila // 2

            es_ultim_pas = (pas_actiu_index is not None and idx == pas_actiu_index)
            if es_ultim_pas:
                resaltat = pygame.Rect(x_esquerra - 10, y_fila + 2, ample_col * 2 + 20, alt_fila - 4)
                pygame.draw.rect(self.pantalla, (232, 248, 245), resaltat, border_radius=6)

            # Factor primer a la dreta de la ratlla vertical
            color_factor = self.VERD if es_ultim_pas else self.LILA
            surf_div = self.font_text_negreta.render(str(divisor), True, color_factor)
            self.pantalla.blit(surf_div, surf_div.get_rect(midleft=(x_dreta, y_centre_fila)))

            # Nou quocient a sota a l'esquerra
            y_seg_centre = y_top + (idx + 1) * alt_fila + alt_fila // 2
            color_quoc = self.BLAU if es_ultim_pas else self.TEXT
            surf_quoc = self.font_text_negreta.render(str(nou_quocient), True, color_quoc)
            self.pantalla.blit(surf_quoc, surf_quoc.get_rect(midright=(x_centre - 18, y_seg_centre)))

        return y_bottom

    def dibuixar_menu_principal(self):
        self._pintar_capcalera("Descomposició en Factors Primers")

        cx = self.amplada // 2
        cy = self.alcada // 2
        w_boto = min(640, int(self.amplada * 0.65))
        h_boto = 105

        r_teoria = pygame.Rect(cx - w_boto // 2, cy - 115, w_boto, h_boto)
        r_exercicis = pygame.Rect(cx - w_boto // 2, cy + 25, w_boto, h_boto)

        self._dibuixar_boto(r_teoria, "1. Teoria (Nombres primers i Descomposició)", self.BLAU, self.BLAU_HOVER)
        self._dibuixar_boto(r_exercicis, "2. Exercicis resolts pas a pas", self.VERD, self.VERD_HOVER)

        peu_txt = "Prem ESC per sortir  ·  Prem F11 per canviar pantalla completa"
        surf_peu = self.font_petita.render(peu_txt, True, self.TEXT_SUAU)
        self.pantalla.blit(surf_peu, surf_peu.get_rect(center=(cx, self.alcada - 42)))

        return {"teoria": r_teoria, "exercicis": r_exercicis}

    def dibuixar_teoria_pagina_1(self, dades):
        self._pintar_capcalera(f"Teoria — Pàgina 1 de 2: {dades['titol']}")

        caixa = pygame.Rect(40, 88, self.amplada - 80, self.alcada - 180)
        pygame.draw.rect(self.pantalla, self.CAIXA, caixa, border_radius=16)
        pygame.draw.rect(self.pantalla, self.VORA, caixa, 2, border_radius=16)

        y_act = self._renderitzar_text_ajustat(
            dades["definicio"],
            self.font_text,
            self.TEXT,
            caixa.x + 28,
            caixa.y + 22,
            caixa.width - 56,
            interlineat=5,
        )

        y_act += 8
        surf_sub = self.font_text_negreta.render(dades["subtitol_llista"], True, self.BLAU)
        self.pantalla.blit(surf_sub, (caixa.x + 28, y_act))
        y_act += surf_sub.get_height() + 10

        # Graella compacta per mostrar tots els nombres primers del 1 al 1000
        primers = dades["primers"]
        marge_x = caixa.x + 28
        ample_util = caixa.width - 56
        ample_cella = 58
        columnes = max(8, ample_util // ample_cella)
        espai_col = ample_util / columnes
        alt_fila = max(20, (caixa.bottom - 14 - y_act) // ((len(primers) // columnes) + 2))

        for i, primer in enumerate(primers):
            col = i % columnes
            fila = i // columnes
            px = int(marge_x + col * espai_col + espai_col / 2)
            py = int(y_act + fila * alt_fila + alt_fila / 2)
            if py + alt_fila // 2 > caixa.bottom - 8:
                break
            surf_p = self.font_petita.render(str(primer), True, self.TEXT)
            self.pantalla.blit(surf_p, surf_p.get_rect(center=(px, py)))

        return self._dibuixar_peu_navegacio(
            te_enrere=True,
            botons_extra=[("pagina_2", "Pàgina 2: Exemple →", self.TARONJA, self.TARONJA_HOVER)],
        )

    def dibuixar_teoria_pagina_2(self, dades):
        self._pintar_capcalera(f"Teoria — Pàgina 2 de 2: {dades['titol']}")

        caixa = pygame.Rect(40, 88, self.amplada - 80, self.alcada - 180)
        pygame.draw.rect(self.pantalla, self.CAIXA, caixa, border_radius=16)
        pygame.draw.rect(self.pantalla, self.VORA, caixa, 2, border_radius=16)

        y_act = self._renderitzar_text_ajustat(
            dades["definicio"],
            self.font_text,
            self.TEXT,
            caixa.x + 28,
            caixa.y + 22,
            caixa.width - 56,
            interlineat=5,
        )

        # Zona inferior dividida en 2 columnes: exemple amb ratlla vertical i resultat final
        y_div = y_act + 14
        pygame.draw.line(self.pantalla, self.VORA, (caixa.x + 24, y_div), (caixa.right - 24, y_div), 2)

        y_contingut = y_div + 18
        alcada_disponible = caixa.bottom - y_contingut - 16
        col_esq_x = caixa.x + int(caixa.width * 0.25)
        col_dreta_x = caixa.x + int(caixa.width * 0.48)
        ample_dreta = caixa.right - col_dreta_x - 30

        surf_tit_ex = self.font_text_negreta.render(f"Exemple complet: {dades['exemple_numero']}", True, self.BLAU)
        self.pantalla.blit(surf_tit_ex, surf_tit_ex.get_rect(center=(col_esq_x, y_contingut + 12)))

        self._dibuixar_taula_descomposicio(
            dades["exemple_numero"],
            dades["exemple_passos"],
            x_centre=col_esq_x,
            y_inici=y_contingut + 40,
            alcada_maxima=alcada_disponible - 40,
        )

        # Explicació de la descomposició obtinguda a la dreta
        surf_res_tit = self.font_mitjana.render("Resultat de la descomposició:", True, self.VERD)
        self.pantalla.blit(surf_res_tit, (col_dreta_x, y_contingut + 10))

        num_ex = dades["exemple_numero"]
        linia_prod = f"{num_ex} = {dades['exemple_producte']}"
        y_d = self._renderitzar_text_ajustat(
            linia_prod,
            self.font_text_negreta,
            self.TEXT,
            col_dreta_x,
            y_contingut + 58,
            ample_dreta,
            interlineat=6,
        )

        linia_pot = f"Amb potències: {num_ex} = {dades['exemple_potencies']}"
        y_d = self._renderitzar_text_ajustat(
            linia_pot,
            self.font_text_negreta,
            self.LILA,
            col_dreta_x,
            y_d + 12,
            ample_dreta,
            interlineat=6,
        )

        nota = "Comprovació: tots els factors de la dreta de la ratlla vertical són nombres primers."
        self._renderitzar_text_ajustat(nota, self.font_petita, self.TEXT_SUAU, col_dreta_x, y_d + 16, ample_dreta)

        return self._dibuixar_peu_navegacio(
            te_enrere=True,
            botons_extra=[("pagina_1", "← Pàgina 1: Primaris", self.BLAU, self.BLAU_HOVER)],
        )

    def dibuixar_exercicis(self, exercici, passos_mostrats):
        self._pintar_capcalera("Exercicis resolts: Descomposició en Factors Primers")

        caixa = pygame.Rect(40, 88, self.amplada - 80, self.alcada - 180)
        pygame.draw.rect(self.pantalla, self.CAIXA, caixa, border_radius=16)
        pygame.draw.rect(self.pantalla, self.VORA, caixa, 2, border_radius=16)

        nombre = exercici["nombre"]
        tots_passos = exercici["passos"]
        mostrats = tots_passos[:passos_mostrats]
        completat = passos_mostrats >= len(tots_passos)

        # Pregunta principal
        pregunta = f"Quina és la descomposició del nombre {nombre}?"
        surf_preg = self.font_mitjana.render(pregunta, True, self.TEXT)
        self.pantalla.blit(surf_preg, (caixa.x + 32, caixa.y + 22))

        estat_pas = f"Pas {passos_mostrats} de {len(tots_passos)}"
        surf_pas = self.font_text_negreta.render(estat_pas, True, self.VERD if completat else self.BLAU)
        self.pantalla.blit(surf_pas, surf_pas.get_rect(topright=(caixa.right - 32, caixa.y + 26)))

        pygame.draw.line(self.pantalla, self.VORA, (caixa.x + 24, caixa.y + 68), (caixa.right - 24, caixa.y + 68), 2)

        # Columna esquerra: ratlla vertical amb els passos mostrats fins ara
        y_taula_inici = caixa.y + 92
        alcada_taula = caixa.bottom - y_taula_inici - 20
        col_esq_x = caixa.x + int(caixa.width * 0.24)
        col_dreta_x = caixa.x + int(caixa.width * 0.45)
        ample_dreta = caixa.right - col_dreta_x - 32

        pas_actiu = passos_mostrats - 1 if passos_mostrats > 0 else None
        self._dibuixar_taula_descomposicio(
            nombre,
            mostrats,
            x_centre=col_esq_x,
            y_inici=y_taula_inici,
            alcada_maxima=alcada_taula,
            pas_actiu_index=pas_actiu,
        )

        # Columna dreta: explicació del pas actual i solució final en nombres primers
        y_r = caixa.y + 95
        if passos_mostrats == 0:
            indicacio = (
                f"Prem el botó \"Següent pas\" per començar a dividir {nombre} "
                "pel nombre primer més petit possible."
            )
            y_r = self._renderitzar_text_ajustat(indicacio, self.font_text, self.TEXT_SUAU, col_dreta_x, y_r, ample_dreta)
        else:
            dividend, divisor, quocient = mostrats[-1]
            explicacio = f"• Dividim {dividend} entre {divisor} (nombre primer) i obtenim {quocient}."
            y_r = self._renderitzar_text_ajustat(explicacio, self.font_text_negreta, self.TEXT, col_dreta_x, y_r, ample_dreta)

            if completat:
                y_r += 16
                surf_sol = self.font_mitjana.render("Descomposició en nombres primers:", True, self.VERD)
                self.pantalla.blit(surf_sol, (col_dreta_x, y_r))
                y_r += surf_sol.get_height() + 10

                y_r = self._renderitzar_text_ajustat(
                    f"{nombre} = {exercici['producte']}",
                    self.font_text_negreta,
                    self.TEXT,
                    col_dreta_x,
                    y_r,
                    ample_dreta,
                )
                self._renderitzar_text_ajustat(
                    f"Forma abreujada amb potències: {nombre} = {exercici['potencies']}",
                    self.font_text_negreta,
                    self.LILA,
                    col_dreta_x,
                    y_r + 6,
                    ample_dreta,
                )

        # 2 botons d'acció principals a la barra inferior: pas a pas i nou exercici
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