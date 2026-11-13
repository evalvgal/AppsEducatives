"""
Accenturació en Català — Interfície gràfica i bucle principal amb Pygame.
Requeriments: pip install pygame
Executar: python grafics_accentuacio.py
"""

import sys
import pygame
from accentuacio import AccentuacioModel, NORMES_ACCENTUACIO

# ==========================================
# CONFIGURACIÓ ARQUITECTÒNICA I UX INFANTIL
# ==========================================
pygame.init()

WIN_W, WIN_H = 1100, 780

info_pantalla = pygame.display.Info()
ancho_pantalla_disponible = info_pantalla.current_w
alto_pantalla_disponible = info_pantalla.current_h

ancho_ventana = min(WIN_W, int(ancho_pantalla_disponible * 0.85))
alto_ventana = min(WIN_H, int(alto_pantalla_disponible * 0.80))

proporcion = WIN_W / WIN_H
if ancho_ventana / alto_ventana > proporcion:
    ancho_ventana = int(alto_ventana * proporcion)
else:
    alto_ventana = int(ancho_ventana / proporcion)

ventana = pygame.display.set_mode((ancho_ventana, alto_ventana), pygame.RESIZABLE)
pantalla = pygame.Surface((WIN_W, WIN_H))

pygame.display.set_caption("🔤 Aprèn a Accentuar en Català!")

# Paleta de colors educativa i suau
BG           = (245, 243, 255)  
TEXT_DARK    = (50,  40,  80)
TEXT_MID     = (110, 100, 140)
CARD_BG      = (255, 255, 255)
CARD_BD      = (190, 180, 220)
BTN_MAIN     = ( 90, 160, 255)
BTN_HOVER    = ( 60, 130, 230)
BTN_ALT      = (120, 210, 140)
BTN_ALT_HOV  = ( 90, 180, 110)
SILABA_BG    = (230, 240, 255)
SILABA_BD    = (120, 160, 220)
ACCENT_COL   = (255,  90,  90)

# Fonts tipogràfiques
fuente_titulo = pygame.font.SysFont("Helvetica", 36, bold=True)
fuente_grande = pygame.font.SysFont("Helvetica", 48, bold=True)
fuente_media  = pygame.font.SysFont("Helvetica", 24, bold=True)
fuente_peque  = pygame.font.SysFont("Helvetica", 17, bold=True)
fuente_silaba = pygame.font.SysFont("Helvetica", 34, bold=True)

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
        pygame.draw.rect(surf, col, self.rect, border_radius=14)
        pygame.draw.rect(surf, TEXT_DARK, self.rect, 2, border_radius=14)
        txt = font.render(self.text, True, (255, 255, 255))
        surf.blit(txt, txt.get_rect(center=self.rect.center))


class AccentuacioAppGrafica:
    def __init__(self) -> None:
        self.model = AccentuacioModel()
        
        self.btn_mode_normes = Button(pygame.Rect(60, 20, 240, 48), "Normes d'Accent", BTN_MAIN, BTN_HOVER)
        self.btn_mode_joc    = Button(pygame.Rect(315, 20, 240, 48), "Mode Joc (Pràctica)", BTN_ALT, BTN_ALT_HOV)
        
        self.btn_ant = Button(pygame.Rect(60, WIN_H - 75, 200, 48), "< Anterior", BTN_MAIN, BTN_HOVER)
        self.btn_seg = Button(pygame.Rect(WIN_W - 260, WIN_H - 75, 200, 48), "Següent >", BTN_MAIN, BTN_HOVER)
        
        self.btn_joc_accio = Button(pygame.Rect(WIN_W // 2 - 175, WIN_H - 85, 350, 52), "Preguntar: Porta accent?", BTN_ALT, BTN_ALT_HOV)

    def obtener_pos_raton_logica(self) -> tuple[int, int]:
        pos_real = pygame.mouse.get_pos()
        w_real, h_real = ventana.get_size()
        x = int(pos_real[0] * (WIN_W / w_real)) if w_real > 0 else 0
        y = int(pos_real[1] * (WIN_H / h_real)) if h_real > 0 else 0
        return (x, y)

    def procesar_eventos(self) -> bool:
        mouse_pos = self.obtener_pos_raton_logica()
        
        self.btn_mode_normes.update(mouse_pos)
        self.btn_mode_joc.update(mouse_pos)
        
        if self.model.mode_actual == "normes":
            self.btn_ant.update(mouse_pos)
            self.btn_seg.update(mouse_pos)
        else:
            self.btn_joc_accio.update(mouse_pos)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.btn_mode_normes.clicked(mouse_pos, evento):
                    self.model.canviar_mode("normes")
                elif self.btn_mode_joc.clicked(mouse_pos, evento):
                    self.model.canviar_mode("joc")
                
                if self.model.mode_actual == "normes":
                    if self.btn_ant.clicked(mouse_pos, evento):
                        self.model.anterior_norma()
                    elif self.btn_seg.clicked(mouse_pos, evento):
                        self.model.seguent_norma()
                else:
                    if self.btn_joc_accio.clicked(mouse_pos, evento):
                        self.model.avançar_pas_joc()
                        # Actualitzem el text del botó segons el pas actual (0, 1, 2, 3)
                        if self.model.joc_pas == 1:
                            self.btn_joc_accio.text = "Preguntar: Porta accent?"
                        elif self.model.joc_pas == 2:
                            self.btn_joc_accio.text = "Veure resposta i raó"
                        elif self.model.joc_pas == 3:
                            self.btn_joc_accio.text = "Veure síl·labes"
                        elif self.model.joc_pas == 0:
                            self.btn_joc_accio.text = "Preguntar: Porta accent?"

        return True

    def renderizar(self) -> None:
        pantalla.fill(BG)
        
        self.btn_mode_normes.draw(pantalla, fuente_peque)
        self.btn_mode_joc.draw(pantalla, fuente_peque)
        
        if self.model.mode_actual == "normes":
            self._renderizar_mode_normes(pantalla)
        else:
            self._renderizar_mode_joc(pantalla)

        ventana.blit(pygame.transform.smoothscale(pantalla, ventana.get_size()), (0, 0))
        pygame.display.flip()

    def _renderizar_mode_normes(self, surf: pygame.Surface) -> None:
        info = self.model.norma_actual_info
        
        card_rect = pygame.Rect(60, 85, WIN_W - 120, 600)
        pygame.draw.rect(surf, CARD_BG, card_rect, border_radius=20)
        pygame.draw.rect(surf, CARD_BD, card_rect, 3, border_radius=20)

        txt_tipus = fuente_titulo.render(info["tipus"], True, TEXT_DARK)
        surf.blit(txt_tipus, (card_rect.x + 40, card_rect.y + 25))

        txt_norma = fuente_media.render(info["norma"], True, TEXT_MID)
        surf.blit(txt_norma, (card_rect.x + 40, card_rect.y + 70))

        txt_ej = fuente_peque.render("Exemples visuals pas a pas:", True, TEXT_DARK)
        surf.blit(txt_ej, (card_rect.x + 40, card_rect.y + 115))

        y_offset = card_rect.y + 145
        for ex in info["exemples"]:
            max_w_arg = 360
            paraules_arg = ex["raquel"].split(" ")
            linies_arg = []
            linia_actual = ""
            for mot in paraules_arg:
                test_linia = f"{linia_actual} {mot}".strip()
                if fuente_peque.size(test_linia)[0] <= max_w_arg:
                    linia_actual = test_linia
                else:
                    linies_arg.append(linia_actual)
                    linia_actual = mot
            if linia_actual:
                linies_arg.append(linia_actual)

            row_h = 58 if len(linies_arg) <= 1 else 72
            row_rect = pygame.Rect(card_rect.x + 25, y_offset, card_rect.w - 50, row_h)
            
            pygame.draw.rect(surf, (250, 248, 255), row_rect, border_radius=12)
            pygame.draw.rect(surf, (220, 210, 240), row_rect, 1, border_radius=12)

            p_surf = fuente_media.render(ex["paraula"], True, TEXT_DARK)
            surf.blit(p_surf, (row_rect.x + 20, row_rect.y + (row_h // 2 - p_surf.get_height() // 2)))

            x_sil = row_rect.x + 190
            for sil in ex["silabes"]:
                s_rect = pygame.Rect(x_sil, row_rect.y + (row_h // 2 - 20), 44, 40)
                pygame.draw.rect(surf, SILABA_BG, s_rect, border_radius=8)
                pygame.draw.rect(surf, SILABA_BD, s_rect, 2, border_radius=8)
                
                col_txt = ACCENT_COL if any(v in sil for v in "àèéíòóú") else TEXT_DARK
                s_surf = fuente_silaba.render(sil, True, col_txt)
                surf.blit(s_surf, s_surf.get_rect(center=s_rect.center))
                x_sil += 50

            arg_y_start = row_rect.y + 12 if len(linies_arg) == 1 else row_rect.y + 8
            for i, linia in enumerate(linies_arg[:2]):
                r_surf = fuente_peque.render(linia, True, TEXT_MID)
                surf.blit(r_surf, (row_rect.x + 420, arg_y_start + (i * 20)))

            y_offset += row_h + 8

        self.btn_ant.draw(surf, fuente_media)
        self.btn_seg.draw(surf, fuente_media)

    def _renderizar_mode_joc(self, surf: pygame.Surface) -> None:
        card_rect = pygame.Rect(100, 100, WIN_W - 200, 580)
        pygame.draw.rect(surf, CARD_BG, card_rect, border_radius=20)
        pygame.draw.rect(surf, CARD_BD, card_rect, 3, border_radius=20)

        instruccio = "Escriu aquesta paraula al teu paper i pensa si s'ha d'accentuar:"
        txt_inst = fuente_media.render(instruccio, True, TEXT_DARK)
        surf.blit(txt_inst, (WIN_W // 2 - txt_inst.get_width() // 2, card_rect.y + 35))

        # La paraula es mostra sempre sense accent a dalt
        paraula_a_mostrar = self.model.paraula_sense_accent
        p_obj = fuente_grande.render(paraula_a_mostrar, True, BTN_MAIN)
        surf.blit(p_obj, (WIN_W // 2 - p_obj.get_width() // 2, card_rect.y + 85))

        # PAS 1 (Primer clic): Només surt la pregunta "PORTA ACCENT?"
        if self.model.joc_pas == 1:
            txt_res = fuente_media.render("PORTA ACCENT?", True, TEXT_DARK)
            surf.blit(txt_res, (WIN_W // 2 - txt_res.get_width() // 2, card_rect.y + 160))

        # PAS 2 (Segon clic): Surt la resposta (SÍ/NO) i l'argumentació (sense mostrar la pregunta prèvia)
        elif self.model.joc_pas == 2:
            accent_status = "PORTA ACCENT? SÍ" if self.model.paraula_actual["accentuada"] else "PORTA ACCENT? NO"
            col_status = ACCENT_COL if self.model.paraula_actual["accentuada"] else (60, 180, 100)
            
            txt_res = fuente_media.render(accent_status, True, col_status)
            surf.blit(txt_res, (WIN_W // 2 - txt_res.get_width() // 2, card_rect.y + 160))

            arg_text = f"Perquè: {self.model.paraula_actual['raquel']}"
            txt_arg = fuente_peque.render(arg_text, True, TEXT_DARK)
            surf.blit(txt_arg, (WIN_W // 2 - txt_arg.get_width() // 2, card_rect.y + 205))

        # PAS 3 (Tercer clic): Es manté la resposta/raó i s'afegeix la descomposició per síl·labes a baix
        elif self.model.joc_pas >= 3:
            accent_status = "PORTA ACCENT? SÍ" if self.model.paraula_actual["accentuada"] else "PORTA ACCENT? NO"
            col_status = ACCENT_COL if self.model.paraula_actual["accentuada"] else (60, 180, 100)
            
            txt_res = fuente_media.render(accent_status, True, col_status)
            surf.blit(txt_res, (WIN_W // 2 - txt_res.get_width() // 2, card_rect.y + 160))

            arg_text = f"Perquè: {self.model.paraula_actual['raquel']}"
            txt_arg = fuente_peque.render(arg_text, True, TEXT_DARK)
            surf.blit(txt_arg, (WIN_W // 2 - txt_arg.get_width() // 2, card_rect.y + 205))

            txt_s_title = fuente_peque.render("Descomposició per síl·labes:", True, TEXT_MID)
            surf.blit(txt_s_title, (WIN_W // 2 - txt_s_title.get_width() // 2, card_rect.y + 260))

            silabes = self.model.paraula_actual["silabes"]
            total_w = len(silabes) * 65
            x_start = WIN_W // 2 - total_w // 2
            for i, sil in enumerate(silabes):
                s_rect = pygame.Rect(x_start + i * 65, card_rect.y + 295, 55, 55)
                pygame.draw.rect(surf, SILABA_BG, s_rect, border_radius=12)
                pygame.draw.rect(surf, SILABA_BD, s_rect, 2, border_radius=12)
                
                col_txt = ACCENT_COL if any(v in sil for v in "àèéíòóú") else TEXT_DARK
                s_surf = fuente_silaba.render(sil, True, col_txt)
                surf.blit(s_surf, s_surf.get_rect(center=s_rect.center))

        self.btn_joc_accio.draw(surf, fuente_media)


def main() -> None:
    app = AccentuacioAppGrafica()
    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        ejecutando = app.procesar_eventos()
        app.renderizar()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()