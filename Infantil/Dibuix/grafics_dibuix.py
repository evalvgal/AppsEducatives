"""
Dibuix Animat per a Educació Infantil — Interfície gràfica amb Pygame.
Executar: python3 grafics_dibuix.py
"""

import sys
import math
import pygame
from dibuix import DibuixModel

pygame.init()

info_pantalla = pygame.display.Info()
FULL_W = info_pantalla.current_w
FULL_H = info_pantalla.current_h

WIN_W = int(FULL_W * 0.85)
WIN_H = int(FULL_H * 0.85)

BLANC_LLENC      = (255, 255, 255)
TEXT_FOSC        = (40, 45, 65)
GRIS_DESACTIVAT  = (190, 195, 205)

COL_SORTIR       = (231, 76, 60)
COL_SORTIR_HOV   = (192, 57, 43)

COL_UNDO_REDO    = (52, 152, 219)
COL_UNDO_HOV     = (41, 128, 185)

COL_LLAPIS       = (46, 204, 113)
COL_GOMA         = (243, 156, 18)
COL_NETEJAR      = (149, 165, 166)
COL_NETEJAR_HOV  = (127, 140, 141)

COL_ANIMAR       = (155, 89, 182)
COL_ANIMAR_HOV   = (142, 68, 173)
COL_ATURAR       = (230, 126, 34)

reloj = pygame.time.Clock()


class BotoUI:
    def __init__(self, rect: pygame.Rect, text: str, color: tuple, hover_color: tuple, actiu: bool = True) -> None:
        self.rect = rect
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.actiu = actiu
        self.hovered = False

    def update(self, mouse_pos: tuple[int, int]) -> None:
        self.hovered = self.actiu and self.rect.collidepoint(mouse_pos)

    def clicat(self, mouse_pos: tuple[int, int], event: pygame.event.Event) -> bool:
        return (
            self.actiu
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(mouse_pos)
        )

    def draw(self, surf: pygame.Surface, font: pygame.font.Font, seleccionat: bool = False) -> None:
        col = GRIS_DESACTIVAT if not self.actiu else (self.hover_color if self.hovered else self.color)
        pygame.draw.rect(surf, col, self.rect, border_radius=14)
        gruix_vora = 4 if seleccionat else 2
        color_vora = (30, 30, 30) if seleccionat else TEXT_FOSC
        pygame.draw.rect(surf, color_vora, self.rect, gruix_vora, border_radius=14)

        txt_surf = font.render(self.text, True, (255, 255, 255))
        surf.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))


class DibuixAppGrafica:
    def __init__(self) -> None:
        self.es_pantalla_completa = True
        self.ventana = pygame.display.set_mode((FULL_W, FULL_H), pygame.FULLSCREEN)
        pygame.display.set_caption("El meu Dibuix Màgic")

        self.model = DibuixModel()
        self.dibuixant = False

        self.font_botons = pygame.font.SysFont("Helvetica", 22, bold=True)
        self.font_avis = pygame.font.SysFont("Helvetica", 26, bold=True)
        self.font_estat = pygame.font.SysFont("Helvetica", 24, bold=True)

        self.colors_paleta = [
            (35, 35, 45),     # Negre
            (30, 60, 180),    # Blau
            (231, 76, 60),    # Vermell
            (39, 174, 96),    # Verd
            (241, 196, 15),   # Groc
            (142, 68, 173)    # Lila
        ]
        self.botons_colors: list[tuple[pygame.Rect, tuple[int, int, int]]] = []
        self._recalcular_disposicio()

    def _recalcular_disposicio(self) -> None:
        w, h = self.ventana.get_size()
        marge = 25
        alt_btn = 54

        self.btn_desfer = BotoUI(pygame.Rect(marge, marge, 135, alt_btn), "Desfer", COL_UNDO_REDO, COL_UNDO_HOV)
        self.btn_refer = BotoUI(pygame.Rect(marge + 150, marge, 135, alt_btn), "Refer", COL_UNDO_REDO, COL_UNDO_HOV)
        self.btn_sortir = BotoUI(pygame.Rect(w - marge - 140, marge, 140, alt_btn), "X Sortir", COL_SORTIR, COL_SORTIR_HOV)

        y_inf = h - marge - alt_btn
        self.btn_goma = BotoUI(pygame.Rect(marge, y_inf, 130, alt_btn), "Goma", COL_GOMA, (211, 84, 0))
        self.btn_netejar = BotoUI(pygame.Rect(marge + 145, y_inf, 165, alt_btn), "Netejar tot", COL_NETEJAR, COL_NETEJAR_HOV)
        self.btn_animar = BotoUI(pygame.Rect(marge + 325, y_inf, 210, alt_btn), "Animar dibuix", COL_ANIMAR, COL_ANIMAR_HOV)

        self.botons_colors.clear()
        radi = 22
        espai = 54
        inici_x = w - marge - (len(self.colors_paleta) * espai) + 15
        centre_y = y_inf + (alt_btn // 2)

        for i, col in enumerate(self.colors_paleta):
            rect_c = pygame.Rect(inici_x + (i * espai) - radi, centre_y - radi, radi * 2, radi * 2)
            self.botons_colors.append((rect_c, col))

    def alternar_pantalla_completa(self) -> None:
        self.es_pantalla_completa = not self.es_pantalla_completa
        if self.es_pantalla_completa:
            self.ventana = pygame.display.set_mode((FULL_W, FULL_H), pygame.FULLSCREEN)
        else:
            self.ventana = pygame.display.set_mode((WIN_W, WIN_H), pygame.RESIZABLE)
        self._recalcular_disposicio()

    def _punt_sobre_ui(self, pos: tuple[int, int]) -> bool:
        botons = [self.btn_desfer, self.btn_refer, self.btn_sortir, self.btn_goma, self.btn_netejar, self.btn_animar]
        if any(b.rect.collidepoint(pos) for b in botons):
            return True
        if any(r.collidepoint(pos) for r, _ in self.botons_colors):
            return True
        return False

    def processar_esdeveniments(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        w, h = self.ventana.get_size()

        self.btn_desfer.actiu = (not self.model.animant) and (len(self.model.tracos) > 0)
        self.btn_refer.actiu = (not self.model.animant) and (len(self.model.tracos_desfets) > 0)
        self.btn_goma.actiu = not self.model.animant
        self.btn_animar.actiu = len(self.model.tracos) > 0
        self.btn_animar.text = "Aturar" if self.model.animant else "Animar dibuix"
        self.btn_animar.color = COL_ATURAR if self.model.animant else COL_ANIMAR

        for btn in [self.btn_desfer, self.btn_refer, self.btn_sortir, self.btn_goma, self.btn_netejar, self.btn_animar]:
            btn.update(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.VIDEORESIZE and not self.es_pantalla_completa:
                self.ventana = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self._recalcular_disposicio()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_F11:
                    self.alternar_pantalla_completa()
                elif event.key == pygame.K_z and (event.mod & pygame.KMOD_CTRL):
                    self.model.desfer()
                elif event.key == pygame.K_y and (event.mod & pygame.KMOD_CTRL):
                    self.model.refer()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.btn_sortir.clicat(mouse_pos, event):
                    return False
                elif self.btn_desfer.clicat(mouse_pos, event):
                    self.model.desfer()
                elif self.btn_refer.clicat(mouse_pos, event):
                    self.model.refer()
                elif self.btn_goma.clicat(mouse_pos, event):
                    self.model.seleccionar_goma()
                elif self.btn_netejar.clicat(mouse_pos, event):
                    self.model.netejar_tot()
                elif self.btn_animar.clicat(mouse_pos, event):
                    self.model.alternar_animacio(w, h)
                else:
                    color_triat = False
                    for rect_c, col in self.botons_colors:
                        if rect_c.collidepoint(mouse_pos):
                            self.model.seleccionar_llapis(col)
                            color_triat = True
                            break

                    if not color_triat and not self._punt_sobre_ui(mouse_pos) and not self.model.animant:
                        self.dibuixant = True
                        self.model.iniciar_trac(mouse_pos, BLANC_LLENC)
            elif event.type == pygame.MOUSEMOTION:
                if self.dibuixant and not self.model.animant:
                    self.model.afegir_punt(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if self.dibuixant:
                    self.dibuixant = False
                    self.model.finalitzar_trac()

        return True

    def _dibuixar_llenc_i_tracos(self) -> None:
        w, h = self.ventana.get_size()
        self.ventana.fill(BLANC_LLENC)

        tots_tracos = list(self.model.tracos)
        if self.model.trac_actual:
            tots_tracos.append(self.model.trac_actual)

        if not tots_tracos:
            avis = self.font_avis.render("Dibuixa el que vulguis i prem 'Animar dibuix'!", True, (180, 185, 200))
            self.ventana.blit(avis, avis.get_rect(center=(w // 2, h // 2)))
            return

        if not self.model.animant:
            for trac in tots_tracos:
                self._renderitzar_trac_individual(self.ventana, trac["punts"], trac["color"], trac["gruix"])
        else:
            # 1. Dibuixar partícules de fons
            for p in self.model.particules:
                pygame.draw.circle(self.ventana, p["color"], (int(p["x"]), int(p["y"])), p["radi"])

            # 2. Calcular límits del dibuix
            tots_punts = [p for t in tots_tracos for p in t["punts"]]
            min_x = min(p[0] for p in tots_punts)
            max_x = max(p[0] for p in tots_punts)
            min_y = min(p[1] for p in tots_punts)
            max_y = max(p[1] for p in tots_punts)
            
            centre_dibuix_x = (min_x + max_x) / 2.0
            alçada_total = max_y - min_y
            if alçada_total == 0: alçada_total = 1

            t = self.model.temps_animacio
            tipus = self.model.tipus_animacio_detectat

            noms_efectes = {
                "onades": "Efecte Onades del Mar detectat!",
                "caminar": "Efecte Anar i Tornar (rebot als cantons)!",
                "ma": "Efecte Mà Detectat! Moviment de dits saludant!",
                "botar": "Efecte Saltar / Botar Alegre detectat!"
            }
            txt_efecte = self.font_estat.render(noms_efectes.get(tipus, ""), True, (120, 50, 160))
            self.ventana.blit(txt_efecte, (w // 2 - txt_efecte.get_width() // 2, 25))

            for trac in tots_tracos:
                punts_transformats = []
                for px, py in trac["punts"]:
                    fx, fy = px, py

                    if tipus == "onades":
                        fy = py + math.sin(t * 5.0 + px * 0.02) * 14.0
                    elif tipus == "caminar":
                        if self.model.direccio_x == -1:
                            dist_centre = px - centre_dibuix_x
                            fx = centre_dibuix_x - dist_centre + self.model.x_transllacio
                        else:
                            fx = px + self.model.x_transllacio

                        rel_y = (py - min_y) / alçada_total
                        rel_x = px - centre_dibuix_x

                        if rel_y > 0.55:
                            pas_cames = math.sin(t * 8.0) * 14.0 * ((rel_y - 0.55) / 0.45)
                            direccio_cama = 1.0 if rel_x >= 0 else -1.0
                            fx += pas_cames * direccio_cama * self.model.direccio_x
                        elif rel_y < 0.35:
                            pas_bracos = math.sin(t * 8.0 + math.pi) * 10.0 * ((0.35 - rel_y) / 0.35)
                            direccio_brac = 1.0 if rel_x >= 0 else -1.0
                            fx += pas_bracos * direccio_brac * self.model.direccio_x

                        fy = py - abs(math.sin(t * 8.0)) * 10.0
                    elif tipus == "ma":
                        rel_y = (py - min_y) / alçada_total
                        if rel_y < 0.45:
                            intensitat_dit = (1.0 - (rel_y / 0.45)) * 16.0
                            fx = px + math.sin(t * 9.0 + px * 0.08) * intensitat_dit
                        else:
                            fy = py + math.sin(t * 4.0) * 4.0
                    else:
                        bot_y = -abs(math.sin(t * 4.5)) * 40.0
                        fy = py + bot_y

                    punts_transformats.append((int(fx), int(fy)))

                self._renderitzar_trac_individual(self.ventana, punts_transformats, trac["color"], trac["gruix"])

    def _renderitzar_trac_individual(self, surf: pygame.Surface, punts: list[tuple[int, int]], color: tuple, gruix: int) -> None:
        if len(punts) == 1:
            pygame.draw.circle(surf, color, punts[0], gruix // 2)
        elif len(punts) > 1:
            pygame.draw.lines(surf, color, False, punts, gruix)
            for p in punts:
                pygame.draw.circle(surf, color, p, gruix // 2)

    def renderitzar(self) -> None:
        self._dibuixar_llenc_i_tracos()

        self.btn_desfer.draw(self.ventana, self.font_botons)
        self.btn_refer.draw(self.ventana, self.font_botons)
        self.btn_sortir.draw(self.ventana, self.font_botons)

        self.btn_goma.draw(self.ventana, self.font_botons, seleccionat=(self.model.eina_activa == "GOMA" and not self.model.animant))
        self.btn_netejar.draw(self.ventana, self.font_botons)
        self.btn_animar.draw(self.ventana, self.font_botons, seleccionat=self.model.animant)

        for rect_c, col in self.botons_colors:
            centre = rect_c.center
            radi = rect_c.width // 2
            pygame.draw.circle(self.ventana, col, centre, radi)
            es_actiu = (self.model.eina_activa == "LLAPIS" and self.model.color_llapis == col and not self.model.animant)
            if es_actiu:
                pygame.draw.circle(self.ventana, TEXT_FOSC, centre, radi + 4, 4)
            else:
                pygame.draw.circle(self.ventana, (200, 200, 210), centre, radi, 2)

        pygame.display.flip()

    def executar(self) -> None:
        executant = True
        while executant:
            dt = reloj.tick(60) / 1000.0
            executant = self.processar_esdeveniments()
            self.model.actualitzar_animacio(dt, *self.ventana.get_size())
            self.renderitzar()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = DibuixAppGrafica()
    app.executar()