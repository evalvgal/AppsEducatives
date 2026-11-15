import pygame
import sys

class VistaDiftongsHiat:
    def __init__(self):
        pygame.init()
        
        # Detecció automàtica de la resolució nativa de la pantalla
        info_pantalla = pygame.display.Info()
        self.amplada = info_pantalla.current_w if info_pantalla.current_w > 0 else 1280
        self.alcada = info_pantalla.current_h if info_pantalla.current_h > 0 else 720

        # Finestra a pantalla completa nativa
        self.pantalla = pygame.display.set_mode((self.amplada, self.alcada), pygame.FULLSCREEN)
        pygame.display.set_caption("Aprèn Diftongs i Hiats - Pissarra Digital")
        
        self.rellotge = pygame.time.Clock()
        
        # Paleta de colors educativa i accessible
        self.BLANC = (255, 255, 255)
        self.BLAU_Fons = (240, 248, 255)
        self.VERMELL_Sortir = (231, 76, 60)
        self.BLAU_Botó = (52, 152, 219)
        self.VERD_Botó = (46, 204, 113)
        self.TARONJA_Botó = (243, 156, 18)
        self.LILA_Botó = (155, 89, 182)
        self.TEXT_Color = (44, 62, 80)
        self.GRIS_Caixa = (255, 255, 255)
        self.GRIS_Vora = (189, 195, 199)

        # Fonts tipogràfiques adaptatives
        try:
            self.font_titol = pygame.font.SysFont("Arial", 50, bold=True)
            self.font_mitjana = pygame.font.SysFont("Arial", 32, bold=True)
            self.font_petita = pygame.font.SysFont("Arial", 24)
            self.font_gran = pygame.font.SysFont("Arial", 60, bold=True)
        except:
            self.font_titol = pygame.font.Font(None, 60)
            self.font_mitjana = pygame.font.SysFont(None, 40)
            self.font_petita = pygame.font.SysFont(None, 28)
            self.font_gran = pygame.font.Font(None, 70)

    def pintar_fons(self, titol_pantalla=""):
        self.pantalla.fill(self.BLAU_Fons)
        if titol_pantalla:
            txt = self.font_titol.render(titol_pantalla, True, self.TEXT_Color)
            self.pantalla.blit(txt, (60, 30))
        self.dibuixar_boto_sortir()

    def obtenir_rect_sortir(self):
        return pygame.Rect(self.amplada - 140, 25, 120, 50)

    def dibuixar_boto_sortir(self):
        rect_sortir = self.obtenir_rect_sortir()
        esta_sobre = rect_sortir.collidepoint(pygame.mouse.get_pos())
        r_actual = rect_sortir.inflate(6, 6) if esta_sobre else rect_sortir
        color = (236, 112, 99) if esta_sobre else self.VERMELL_Sortir

        pygame.draw.rect(self.pantalla, color, r_actual, border_radius=12)
        txt = self.font_mitjana.render("Sortir", True, self.BLANC)
        self.pantalla.blit(txt, txt.get_rect(center=r_actual.center))
        return rect_sortir

    def dibuixar_boto_enrere(self):
        rect_enrere = pygame.Rect(50, self.alcada - 80, 160, 50)
        esta_sobre = rect_enrere.collidepoint(pygame.mouse.get_pos())
        r_actual = rect_enrere.inflate(6, 6) if esta_sobre else rect_enrere
        color = (210, 215, 220) if esta_sobre else self.GRIS_Vora

        pygame.draw.rect(self.pantalla, color, r_actual, border_radius=12)
        txt = self.font_mitjana.render("← Menú", True, self.TEXT_Color)
        self.pantalla.blit(txt, txt.get_rect(center=r_actual.center))
        return rect_enrere

    def dibuixar_menu_principal(self):
        self.pintar_fons("Reforç Lingüístic: Diftongs i Hiats")
        
        w_b, h_b = 600, 120
        cx = self.amplada // 2
        cy = self.alcada // 2

        boto_diftongs = pygame.Rect(cx - w_b // 2, cy - 140, w_b, h_b)
        boto_hiats = pygame.Rect(cx - w_b // 2, cy, w_b, h_b)
        boto_exercicis = pygame.Rect(cx - w_b // 2, cy + 140, w_b, h_b)

        pos_ratoli = pygame.mouse.get_pos()

        def dibuixar_boto_interactiu(rect, color_base, color_hover, text):
            esta_sobre = rect.collidepoint(pos_ratoli)
            r_actual = rect.inflate(10, 10) if esta_sobre else rect
            color_actual = color_hover if esta_sobre else color_base
            
            pygame.draw.rect(self.pantalla, color_actual, r_actual, border_radius=20)
            txt_surf = self.font_mitjana.render(text, True, self.BLANC)
            self.pantalla.blit(txt_surf, txt_surf.get_rect(center=r_actual.center))
            return rect

        dibuixar_boto_interactiu(boto_diftongs, self.BLAU_Botó, (93, 173, 226), "1. Diftongs (Creixents i Decreixents)")
        dibuixar_boto_interactiu(boto_hiats, self.TARONJA_Botó, (248, 196, 113), "2. Els Hiats i Exemples")
        dibuixar_boto_interactiu(boto_exercicis, self.VERD_Botó, (88, 214, 141), "3. Zona d'Exercicis Pràctics")

        return boto_diftongs, boto_hiats, boto_exercicis

    def dibuixar_pantalla_diftongs(self, dades):
        self.pintar_fons("Teoria: Els Diftongs")
        
        ample_caixa = (self.amplada - 150) // 2
        alcada_caixa = self.alcada - 220
        y_pos = 110

        caixa1 = pygame.Rect(50, y_pos, ample_caixa, alcada_caixa)
        caixa2 = pygame.Rect(100 + ample_caixa, y_pos, ample_caixa, alcada_caixa)

        pygame.draw.rect(self.pantalla, self.GRIS_Caixa, caixa1, border_radius=15)
        pygame.draw.rect(self.pantalla, self.GRIS_Vora, caixa1, 2, border_radius=15)
        
        pygame.draw.rect(self.pantalla, self.GRIS_Caixa, caixa2, border_radius=15)
        pygame.draw.rect(self.pantalla, self.GRIS_Vora, caixa2, 2, border_radius=15)

        # Contingut Requadre 1: Decreixents
        dec = dades["decreixents"]
        self._renderitzar_text_multilinia(dec["títol"], self.font_mitjana, self.TEXT_Color, caixa1.x + 30, caixa1.y + 30)
        self._renderitzar_text_multilinia(dec["definicio"], self.font_petita, self.TEXT_Color, caixa1.x + 30, caixa1.y + 90, caixa1.width - 60)
        self._renderitzar_text_multilinia(dec["classificacio"], self.font_petita, self.TEXT_Color, caixa1.x + 30, caixa1.y + 220, caixa1.width - 60)
        
        y_ex = caixa1.y + 330
        self._renderitzar_text_multilinia("Exemples de separació:", self.font_mitjana, self.TARONJA_Botó, caixa1.x + 30, y_ex)
        for ex in dec["exemples"]:
            y_ex += 45
            txt_ex = f"• {ex['paraula']}  ➔  {ex['silabes']}"
            self._renderitzar_text_multilinia(txt_ex, self.font_petita, self.TEXT_Color, caixa1.x + 50, y_ex)

        # Contingut Requadre 2: Creixents
        cre = dades["creixents"]
        self._renderitzar_text_multilinia(cre["títol"], self.font_mitjana, self.TEXT_Color, caixa2.x + 30, caixa2.y + 30)
        self._renderitzar_text_multilinia(cre["definicio"], self.font_petita, self.TEXT_Color, caixa2.x + 30, caixa2.y + 90, caixa2.width - 60)
        self._renderitzar_text_multilinia(cre["classificacio"], self.font_petita, self.TEXT_Color, caixa2.x + 30, caixa2.y + 220, caixa2.width - 60)
        
        y_ex2 = caixa2.y + 330
        self._renderitzar_text_multilinia("Exemples de separació:", self.font_mitjana, self.TARONJA_Botó, caixa2.x + 30, y_ex2)
        for ex in cre["exemples"]:
            y_ex2 += 45
            txt_ex = f"• {ex['paraula']}  ➔  {ex['silabes']}"
            self._renderitzar_text_multilinia(txt_ex, self.font_petita, self.TEXT_Color, caixa2.x + 50, y_ex2)

        return self.dibuixar_boto_enrere()

    def dibuixar_pantalla_hiats(self, dades):
        self.pintar_fons("Teoria i Exemples: Els Hiats")
        
        caixa = pygame.Rect(50, 110, self.amplada - 100, self.alcada - 220)
        pygame.draw.rect(self.pantalla, self.GRIS_Caixa, caixa, border_radius=15)
        pygame.draw.rect(self.pantalla, self.GRIS_Vora, caixa, 2, border_radius=15)

        self._renderitzar_text_multilinia(dades["títol"], self.font_mitjana, self.TARONJA_Botó, caixa.x + 40, caixa.y + 30)
        self._renderitzar_text_multilinia(dades["definicio"], self.font_petita, self.TEXT_Color, caixa.x + 40, caixa.y + 80, caixa.width - 80)

        self._renderitzar_text_multilinia("10 Exemples de paraules amb hiat i la seva separació sil·làbica:", self.font_mitjana, self.BLAU_Botó, caixa.x + 40, caixa.y + 160)

        exemples = dades["exemples"]
        mig_x = caixa.x + caixa.width // 2
        for i, ex in enumerate(exemples):
            col = 0 if i < 5 else 1
            fila = i % 5
            px = caixa.x + 50 if col == 0 else mig_x + 30
            py = caixa.y + 220 + (fila * 45)
            txt = f"{i+1}. {ex['paraula']}  ➔  {ex['silabes']}"
            self._renderitzar_text_multilinia(txt, self.font_petita, self.TEXT_Color, px, py)

        return self.dibuixar_boto_enrere()

    def dibuixar_pantalla_exercici(self, paraula_actual, estat_feedback, tipus_seleccionat="", text_silabes=""):
        self.pintar_fons("Pràctica: Identifica i Separa")
        
        ample_caixa = 1040
        caixa = pygame.Rect(self.amplada // 2 - ample_caixa // 2, 105, ample_caixa, self.alcada - 195)
        pygame.draw.rect(self.pantalla, self.GRIS_Caixa, caixa, border_radius=15)
        pygame.draw.rect(self.pantalla, self.GRIS_Vora, caixa, 2, border_radius=15)

        txt_p = self.font_petita.render("1. Selecciona el fenomen i 2. Separa la paraula per síl·labes:", True, self.TEXT_Color)
        self.pantalla.blit(txt_p, (caixa.x + 40, caixa.y + 20))

        paraula_txt = self.font_gran.render(paraula_actual["paraula"].upper(), True, self.BLAU_Botó)
        self.pantalla.blit(paraula_txt, paraula_txt.get_rect(center=(caixa.centerx, caixa.y + 85)))

        w_btn, h_btn = 290, 52
        espaiat = 25
        ample_total_btns = (3 * w_btn) + (2 * espaiat)
        inici_x_btns = caixa.centerx - ample_total_btns // 2
        y_btns = caixa.y + 140

        b_creixent = pygame.Rect(inici_x_btns, y_btns, w_btn, h_btn)
        b_decreixent = pygame.Rect(inici_x_btns + w_btn + espaiat, y_btns, w_btn, h_btn)
        b_hiat = pygame.Rect(inici_x_btns + (w_btn + espaiat) * 2, y_btns, w_btn, h_btn)

        pos_ratoli = pygame.mouse.get_pos()

        def dibuixar_boto_fenomen(rect, color_base, color_hover, text, seleccionat):
            esta_sobre = rect.collidepoint(pos_ratoli)
            r_actual = rect.inflate(8, 8) if (esta_sobre or seleccionat) else rect
            color_actual = color_hover if esta_sobre else color_base

            pygame.draw.rect(self.pantalla, color_actual, r_actual, border_radius=12)
            if seleccionat:
                pygame.draw.rect(self.pantalla, self.TEXT_Color, r_actual, 3, border_radius=12)
            
            txt_s = self.font_petita.render(text, True, self.BLANC)
            self.pantalla.blit(txt_s, txt_s.get_rect(center=r_actual.center))

        dibuixar_boto_fenomen(b_creixent, self.LILA_Botó, (187, 143, 206), "Diftong Creixent", tipus_seleccionat == "creixent")
        dibuixar_boto_fenomen(b_decreixent, self.TARONJA_Botó, (248, 196, 113), "Diftong Decreixent", tipus_seleccionat == "decreixent")
        dibuixar_boto_fenomen(b_hiat, self.VERD_Botó, (88, 214, 141), "Hiat", tipus_seleccionat == "hiat")

        # Doble requadre de resposta
        y_labels = caixa.y + 215
        y_inputs = caixa.y + 250
        marge_lat = 40
        sep_mig = 30
        ample_col = (caixa.width - (2 * marge_lat) - sep_mig) // 2

        col1_x = caixa.x + marge_lat
        col2_x = col1_x + ample_col + sep_mig

        self.pantalla.blit(self.font_petita.render("Fenomen seleccionat:", True, self.TEXT_Color), (col1_x, y_labels))
        self.pantalla.blit(self.font_petita.render("Separació sil·làbica (amb guions):", True, self.TEXT_Color), (col2_x, y_labels))

        # Requadre 1: Fenomen
        rect_fenomen = pygame.Rect(col1_x, y_inputs, ample_col, 55)
        pygame.draw.rect(self.pantalla, (245, 247, 250), rect_fenomen, border_radius=10)
        pygame.draw.rect(self.pantalla, self.GRIS_Vora, rect_fenomen, 2, border_radius=10)

        noms_fenomen = {
            "creixent": "DIFTONG CREIXENT",
            "decreixent": "DIFTONG DECREIXENT",
            "hiat": "HIAT"
        }
        text_fen = noms_fenomen.get(tipus_seleccionat, "Prem un botó de dalt...")
        col_fen = self.TEXT_Color if tipus_seleccionat else (150, 150, 150)
        surf_fen = self.font_petita.render(text_fen, True, col_fen)
        self.pantalla.blit(surf_fen, surf_fen.get_rect(center=rect_fenomen.center))

        # Requadre 2: Síl·labes
        rect_silabes = pygame.Rect(col2_x, y_inputs, ample_col, 55)
        pygame.draw.rect(self.pantalla, self.BLANC, rect_silabes, border_radius=10)
        pygame.draw.rect(self.pantalla, self.BLAU_Botó if estat_feedback is None else self.GRIS_Vora, rect_silabes, 2, border_radius=10)

        text_sil = text_silabes if text_silabes else "Escriu aquí (ex: quo-ta)..."
        col_sil = self.TEXT_Color if text_silabes else (150, 150, 150)
        surf_sil = self.font_petita.render(text_sil, True, col_sil)
        self.pantalla.blit(surf_sil, surf_sil.get_rect(center=rect_silabes.center))

        # Feedback individual sota cada requadre
        if estat_feedback:
            y_fb = y_inputs + 68
            col_fb1 = self.VERD_Botó if estat_feedback["fenomen_ok"] else self.VERMELL_Sortir
            self._renderitzar_text_multilinia(estat_feedback["msg_fenomen"], self.font_petita, col_fb1, col1_x, y_fb, ample_col)

            col_fb2 = self.VERD_Botó if estat_feedback["silabes_ok"] else self.VERMELL_Sortir
            self._renderitzar_text_multilinia(estat_feedback["msg_silabes"], self.font_petita, col_fb2, col2_x, y_fb, ample_col)

        # Botó Validar / Següent interactiu
        b_validar = pygame.Rect(caixa.centerx - 190, caixa.y + caixa.height - 70, 380, 52)
        text_btn_val = "Següent Paraula" if estat_feedback is not None else "Comprovar Resposta"
        
        esta_sobre_val = b_validar.collidepoint(pos_ratoli)
        r_val_actual = b_validar.inflate(8, 8) if esta_sobre_val else b_validar
        color_val_base = self.BLAU_Botó if estat_feedback is not None else self.VERD_Botó
        color_val_hover = (93, 173, 226) if estat_feedback is not None else (88, 214, 141)

        pygame.draw.rect(self.pantalla, color_val_hover if esta_sobre_val else color_val_base, r_val_actual, border_radius=15)
        txt_val = self.font_mitjana.render(text_btn_val, True, self.BLANC)
        self.pantalla.blit(txt_val, txt_val.get_rect(center=r_val_actual.center))

        return b_creixent, b_decreixent, b_hiat, b_validar, self.dibuixar_boto_enrere()

    def _renderitzar_text_multilinia(self, text, font, color, x, y, max_ample=1000):
        Paraules = text.split(' ')
        linia_actual = []
        for paraula in Paraules:
            prova_linia = ' '.join(linia_actual + [paraula])
            if font.size(prova_linia)[0] < max_ample:
                linia_actual.append(paraula)
            else:
                txt_surf = font.render(' '.join(linia_actual), True, color)
                self.pantalla.blit(txt_surf, (x, y))
                y += font.get_linesize() + 4
                linia_actual = [paraula]
        if linia_actual:
            txt_surf = font.render(' '.join(linia_actual), True, color)
            self.pantalla.blit(txt_surf, (x, y))

    def actualitzar_pantalla(self):
        pygame.display.flip()
        self.rellotge.tick(60)