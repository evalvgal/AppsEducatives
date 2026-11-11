"""
Accents Diacrítics en Català — Interfície gràfica amb Pygame (Ressaltat intel·ligent de paraules per a l'aula).
Executar: python grafics_diacritics.py
"""

import sys
import pygame
from diacritics import DiacriticsModel

pygame.init()

WIN_W, WIN_H = 1100, 780

info = pygame.display.Info()
w_disponible, h_disponible = info.current_w, info.current_h
w_v = min(WIN_W, int(w_disponible * 0.85))
h_v = min(WIN_H, int(h_disponible * 0.80))

prop = WIN_W / WIN_H
if w_v / h_v > prop:
    w_v = int(h_v * prop)
else:
    h_v = int(w_v / prop)

ventana = pygame.display.set_mode((w_v, h_v), pygame.RESIZABLE)
pantalla = pygame.Surface((WIN_W, WIN_H))
pygame.display.set_caption("🔤 Els Accents Diacrítics en Català")

# Colors suaus i educatius
BG          = (245, 243, 255)
TEXT_DARK   = (40, 35, 70)
TEXT_MID    = (70, 65, 100)
TEXT_GRAY   = (110, 110, 130)  # Color gris suau per al text general
CARD_BG     = (255, 255, 255)

# Targeta Blava (Accent Diacrític)
ACCENT_BG   = (238, 244, 255)
ACCENT_BD   = (140, 175, 240)
ACCENT_COL  = (25, 90, 210)

# Targeta Verda (Sense Accent)
NO_ACC_BG   = (240, 250, 242)
NO_ACC_BD   = (150, 210, 160)
NO_ACC_COL  = (30, 140, 60)

# Botons generals i estat actiu en verd
BTN_MAIN    = (90, 150, 240)
BTN_HOVER   = (60, 120, 220)
GREEN_ACTIVE = (40, 180, 80)
GREEN_HOVER  = (30, 150, 65)

# Fonts tipogràfiques grans i llegibles
font_paraula = pygame.font.SysFont("Helvetica", 64, bold=True)
font_sub     = pygame.font.SysFont("Helvetica", 24, bold=True)
font_text    = pygame.font.SysFont("Helvetica", 22, bold=True)
font_peque   = pygame.font.SysFont("Helvetica", 18, bold=True)

reloj = pygame.time.Clock()


class Button:
    def __init__(self, rect: pygame.Rect, text: str, color: tuple, hover_col: tuple) -> None:
        self.rect = rect
        self.text = text
        self.color = color
        self.hover_col = hover_col
        self._hovered = False

    def update(self, mouse_pos: tuple[int, int]) -> None:
        self._hovered = self.rect.collidepoint(mouse_pos)

    def clicked(self, mouse_pos: tuple[int, int], event: pygame.event.Event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(mouse_pos))

    def draw(self, surf: pygame.Surface, font: pygame.font.Font) -> None:
        col = self.hover_col if self._hovered else self.color
        pygame.draw.rect(surf, col, self.rect, border_radius=12)
        pygame.draw.rect(surf, TEXT_DARK, self.rect, 2, border_radius=12)
        txt = font.render(self.text, True, (255, 255, 255))
        surf.blit(txt, txt.get_rect(center=self.rect.center))


class DiacriticsAppGrafica:
    def __init__(self) -> None:
        self.model = DiacriticsModel()
        
        self.btn_ant = Button(pygame.Rect(50, WIN_H - 70, 160, 42), "< Anterior", BTN_MAIN, BTN_HOVER)
        self.btn_seg = Button(pygame.Rect(WIN_W - 210, WIN_H - 70, 160, 42), "Següent >", BTN_MAIN, BTN_HOVER)

        self.btn_pagines = []
        total_nums = 15
        ample_btn = 30
        espaiat = 5
        ample_total = (total_nums * ample_btn) + ((total_nums - 1) * espaiat)
        start_x = (WIN_W // 2) - (ample_total // 2)
        y_pos = WIN_H - 70

        for i in range(total_nums):
            rect_b = pygame.Rect(start_x + (i * (ample_btn + espaiat)), y_pos, ample_btn, 42)
            self.btn_pagines.append((i, rect_b))

    def obtenir_pos_raton_logica(self) -> tuple[int, int]:
        pos_real = pygame.mouse.get_pos()
        w_real, h_real = ventana.get_size()
        x = int(pos_real[0] * (WIN_W / w_real)) if w_real > 0 else 0
        y = int(pos_real[1] * (WIN_H / h_real)) if h_real > 0 else 0
        return (x, y)

    def procesar_eventos(self) -> bool:
        mouse_pos = self.obtenir_pos_raton_logica()
        self.btn_ant.update(mouse_pos)
        self.btn_seg.update(mouse_pos)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.btn_ant.clicked(mouse_pos, evento):
                    self.model.anterior_pagina()
                elif self.btn_seg.clicked(mouse_pos, evento):
                    self.model.seguent_pagina()
                
                for idx, rect in self.btn_pagines:
                    if rect.collidepoint(mouse_pos):
                        self.model.anar_a_pagina(idx)

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    self.model.anterior_pagina()
                elif evento.key == pygame.K_RIGHT:
                    self.model.seguent_pagina()

        return True

    def _dibuixar_exemple_intelligent(self, surf: pygame.Surface, x: int, y: int, prefix: str, frase: str, paraula_objectiu: str, color_resaltat: tuple) -> None:
        """Processa la frase paraula a paraula per ressaltar exactament la paraula diacrítica independentment de majúscules o puntuació."""
        pref_surf = font_text.render(prefix, True, TEXT_GRAY)
        surf.blit(pref_surf, (x, y))
        x_actual = x + pref_surf.get_width()

        paraules = frase.split(" ")
        target_clean = ''.join(c for c in paraula_objectiu.lower() if c.isalnum() or c in "àèéíòóúïüçàèéíòóú'")
        espai_ample = font_text.size(" ")[0]

        for w in paraules:
            clean_w = ''.join(c for c in w.lower() if c.isalnum() or c in "àèéíòóúïüçàèéíòóú'")
            parts = clean_w.split("'")
            is_match = (clean_w == target_clean or target_clean in parts)

            color_paraula = color_resaltat if is_match else TEXT_GRAY
            w_surf = font_text.render(w, True, color_paraula)
            surf.blit(w_surf, (x_actual, y))
            x_actual += w_surf.get_width() + espai_ample

    def _dibuixar_detalls_targeta(self, surf: pygame.Surface, card_rect: pygame.Rect, dades: dict, color_principal: tuple) -> None:
        """Dibuixa el contingut de la targeta."""
        p_surf = font_paraula.render(dades["paraula"], True, color_principal)
        surf.blit(p_surf, (card_rect.x + 30, card_rect.y + 70))

        cat_surf = font_sub.render(f"({dades['categoria']})", True, TEXT_MID)
        surf.blit(cat_surf, (card_rect.x + 30, card_rect.y + 145))

        def_surf = font_text.render(f"Significat: {dades['def']}", True, TEXT_DARK)
        surf.blit(def_surf, (card_rect.x + 30, card_rect.y + 210))

        exemples = dades["exemples"]
        paraula_clau = dades["paraula"]
        y_offset = 275

        if len(exemples) == 1:
            self._dibuixar_exemple_intelligent(surf, card_rect.x + 30, card_rect.y + y_offset, "Exemple: ", exemples[0], paraula_clau, color_principal)
        else:
            self._dibuixar_exemple_intelligent(surf, card_rect.x + 30, card_rect.y + y_offset, "Exemple 1: ", exemples[0], paraula_clau, color_principal)
            self._dibuixar_exemple_intelligent(surf, card_rect.x + 30, card_rect.y + y_offset + 55, "Exemple 2: ", exemples[1], paraula_clau, color_principal)

    def renderizar(self) -> None:
        pantalla.fill(BG)
        parell = self.model.parell_actual

        # Targeta Esquerra: AMB ACCENT (Tons Blaus)
        card_l = pygame.Rect(50, 20, 480, 595)
        pygame.draw.rect(pantalla, ACCENT_BG, card_l, border_radius=20)
        pygame.draw.rect(pantalla, ACCENT_BD, card_l, 3, border_radius=20)

        badge_l = font_peque.render("AMB ACCENT DIACRÍTIC", True, (255, 255, 255))
        badge_rect_l = pygame.Rect(card_l.x + 25, card_l.y + 22, 220, 32)
        pygame.draw.rect(pantalla, ACCENT_COL, badge_rect_l, border_radius=8)
        pantalla.blit(badge_l, badge_l.get_rect(center=badge_rect_l.center))

        self._dibuixar_detalls_targeta(pantalla, card_l, parell["amb_accent"], ACCENT_COL)

        # Targeta Dreta: SENSE ACCENT (Tons Verds)
        card_r = pygame.Rect(570, 20, 480, 595)
        pygame.draw.rect(pantalla, NO_ACC_BG, card_r, border_radius=20)
        pygame.draw.rect(pantalla, NO_ACC_BD, card_r, 3, border_radius=20)

        badge_r = font_peque.render("SENSE ACCENT", True, (255, 255, 255))
        badge_rect_r = pygame.Rect(card_r.x + 25, card_r.y + 22, 170, 32)
        pygame.draw.rect(pantalla, NO_ACC_COL, badge_rect_r, border_radius=8)
        pantalla.blit(badge_r, badge_r.get_rect(center=badge_rect_r.center))

        self._dibuixar_detalls_targeta(pantalla, card_r, parell["sense_accent"], NO_ACC_COL)

        info_pag = f"Pàgina {self.model.pagina_actual + 1} de {self.model.total_pagines}"
        txt_pag = font_sub.render(info_pag, True, TEXT_MID)
        pantalla.blit(txt_pag, (WIN_W // 2 - txt_pag.get_width() // 2, WIN_H - 105))

        self.btn_ant.draw(pantalla, font_peque)
        self.btn_seg.draw(pantalla, font_peque)

        mouse_pos = self.obtenir_pos_raton_logica()
        for idx, rect in self.btn_pagines:
            es_actiu = (idx == self.model.pagina_actual)
            is_hover = rect.collidepoint(mouse_pos)

            if es_actiu:
                col_fons = GREEN_ACTIVE
            elif is_hover:
                col_fons = GREEN_HOVER
            else:
                col_fons = CARD_BG

            col_text = (255, 255, 255) if es_actiu or is_hover else TEXT_DARK

            pygame.draw.rect(pantalla, col_fons, rect, border_radius=8)
            pygame.draw.rect(pantalla, GREEN_ACTIVE if es_actiu else TEXT_DARK, rect, 2, border_radius=8)

            txt_num = font_peque.render(str(idx + 1), True, col_text)
            pantalla.blit(txt_num, txt_num.get_rect(center=rect.center))

        ventana.blit(pygame.transform.smoothscale(pantalla, ventana.get_size()), (0, 0))
        pygame.display.flip()


def main() -> None:
    app = DiacriticsAppGrafica()
    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        ejecutando = app.procesar_eventos()
        app.renderizar()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()