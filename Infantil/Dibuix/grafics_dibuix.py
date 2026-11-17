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
COL_PERSONATGE   = (39, 174, 96)
COL_PERS_HOV     = (30, 140, 75)
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

        self.font_botons = pygame.font.SysFont("Helvetica", 17, bold=True)  # Font lleugerament optimitzada per encabir el text llarg
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

        self.btn_desfer = BotoUI(pygame.Rect(marge, marge, 120, alt_btn), "Desfer", COL_UNDO_REDO, COL_UNDO_HOV)
        self.btn_refer = BotoUI(pygame.Rect(marge + 132, marge, 120, alt_btn), "Refer", COL_UNDO_REDO, COL_UNDO_HOV)
        self.btn_sortir = BotoUI(pygame.Rect(w - marge - 130, marge, 130, alt_btn), "X Sortir", COL_SORTIR, COL_SORTIR_HOV)

        y_inf = h - marge - alt_btn
        self.btn_goma = BotoUI(pygame.Rect(marge, y_inf, 105, alt_btn), "Goma", COL_GOMA, (211, 84, 0))
        self.btn_netejar = BotoUI(pygame.Rect(marge + 115, y_inf, 135, alt_btn), "Netejar", COL_NETEJAR, COL_NETEJAR_HOV)
        self.btn_animar = BotoUI(pygame.Rect(marge + 260, y_inf, 160, alt_btn), "Animar dibuix", COL_ANIMAR, COL_ANIMAR_HOV)
        
        # Botó ample dedicat per encabir "A-Z / 0-9 / Figures"
        self.btn_personatge = BotoUI(pygame.Rect(marge + 430, y_inf, 235, alt_btn), "A-Z / 0-9 / Figures", COL_PERSONATGE, COL_PERS_HOV)

        self.botons_colors.clear()
        radi = 20
        espai = 46
        inici_x = w - marge - (len(self.colors_paleta) * espai) + 12
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
        botons = [
            self.btn_desfer, self.btn_refer, self.btn_sortir,
            self.btn_goma, self.btn_netejar, self.btn_animar, self.btn_personatge
        ]
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
        self.btn_personatge.actiu = len(self.model.tracos) > 0

        self.btn_animar.text = "Aturar" if self.model.animant else "Animar dibuix"
        self.btn_animar.color = COL_ATURAR if self.model.animant else COL_ANIMAR

        for btn in [self.btn_desfer, self.btn_refer, self.btn_sortir, self.btn_goma, self.btn_netejar, self.btn_animar, self.btn_personatge]:
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
                elif self.btn_personatge.clicat(mouse_pos, event):
                    self.model.alternar_animacio(w, h, forcar_tipus="lletra")
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

    def _dibuixar_anatomia_personatge(
        self,
        surf: pygame.Surface,
        min_x: float,
        max_x: float,
        min_y: float,
        max_y: float,
        t: float,
        direccio: int,
        desfasament: float = 0.0
    ) -> None:
        """Dibuixa braços, cames, ulls i boca sobre cada lletra, nombre o figura geomètrica."""
        cx = (min_x + max_x) / 2.0
        ample = max(45.0, max_x - min_x)
        alcada = max(70.0, max_y - min_y)

        fase = t * 8.5 + desfasament
        pas_cama = math.sin(fase) * 20.0
        aixecar_peu_1 = max(0.0, math.cos(fase) * 9.0)
        aixecar_peu_2 = max(0.0, -math.cos(fase) * 9.0)

        color_extremitats = (45, 50, 70)
        color_sabates = (231, 76, 60)
        color_guants = (241, 196, 15)

        # Cames i sabates
        maluc_y = max_y - 4
        llarg_cama = min(50.0, alcada * 0.34)
        sep_maluc = min(22.0, ample * 0.24)

        maluc_e = (int(cx - sep_maluc), int(maluc_y))
        peu_e = (int(cx - sep_maluc - pas_cama), int(maluc_y + llarg_cama - aixecar_peu_1))
        pygame.draw.line(surf, color_extremitats, maluc_e, peu_e, 6)
        pygame.draw.ellipse(surf, color_sabates, pygame.Rect(peu_e[0] - 11 + direccio * 4, peu_e[1] - 6, 22, 13))
        pygame.draw.ellipse(surf, color_extremitats, pygame.Rect(peu_e[0] - 11 + direccio * 4, peu_e[1] - 6, 22, 13), 2)

        maluc_d = (int(cx + sep_maluc), int(maluc_y))
        peu_d = (int(cx + sep_maluc + pas_cama), int(maluc_y + llarg_cama - aixecar_peu_2))
        pygame.draw.line(surf, color_extremitats, maluc_d, peu_d, 6)
        pygame.draw.ellipse(surf, color_sabates, pygame.Rect(peu_d[0] - 11 + direccio * 4, peu_d[1] - 6, 22, 13))
        pygame.draw.ellipse(surf, color_extremitats, pygame.Rect(peu_d[0] - 11 + direccio * 4, peu_d[1] - 6, 22, 13), 2)

        # Braços i mans
        espatlla_y = min_y + alcada * 0.50
        llarg_brac = min(40.0, ample * 0.35 + 16.0)

        esp_e = (int(min_x + 4), int(espatlla_y))
        ma_e = (int(min_x - llarg_brac * 0.7 + pas_cama * 0.75), int(espatlla_y + llarg_brac * 0.45))
        pygame.draw.line(surf, color_extremitats, esp_e, ma_e, 5)
        pygame.draw.circle(surf, color_guants, ma_e, 8)
        pygame.draw.circle(surf, color_extremitats, ma_e, 8, 2)

        esp_d = (int(max_x - 4), int(espatlla_y))
        ma_d = (int(max_x + llarg_brac * 0.7 - pas_cama * 0.75), int(espatlla_y + llarg_brac * 0.45))
        pygame.draw.line(surf, color_extremitats, esp_d, ma_d, 5)
        pygame.draw.circle(surf, color_guants, ma_d, 8)
        pygame.draw.circle(surf, color_extremitats, ma_d, 8, 2)

        # Ulls i boca
        cara_x = int(cx + direccio * 5)
        ulls_y = int(min_y + alcada * 0.36)
        sep_ulls = min(14, int(ample * 0.22))
        radi_ull = 9

        parpellejant = ((t + desfasament * 0.2) % 3.5) > 3.35

        for dx in (-sep_ulls, sep_ulls):
            ux = cara_x + dx
            if parpellejant:
                pygame.draw.line(surf, color_extremitats, (ux - 7, ulls_y), (ux + 7, ulls_y), 3)
            else:
                pygame.draw.circle(surf, (255, 255, 255), (ux, ulls_y), radi_ull)
                pygame.draw.circle(surf, color_extremitats, (ux, ulls_y), radi_ull, 2)
                pygame.draw.circle(surf, (25, 25, 35), (ux + direccio * 3, ulls_y), 4)
                pygame.draw.circle(surf, (255, 255, 255), (ux + direccio * 2, ulls_y - 2), 2)

        boca_rect = pygame.Rect(cara_x - 14, ulls_y + 10, 28, 17)
        pygame.draw.arc(surf, color_extremitats, boca_rect, math.pi, 2 * math.pi, 3)

    def _dibuixar_llenc_i_tracos(self) -> None:
        w, h = self.ventana.get_size()
        self.ventana.fill(BLANC_LLENC)

        tots_tracos = list(self.model.tracos)
        if self.model.trac_actual:
            tots_tracos.append(self.model.trac_actual)

        if not tots_tracos:
            avis = self.font_avis.render("Dibuixa caràcters (A-Z, 0-9), figures o dibuixos i prem 'Animar'!", True, (180, 185, 200))
            self.ventana.blit(avis, avis.get_rect(center=(w // 2, h // 2)))
            return

        if not self.model.animant:
            for trac in tots_tracos:
                self._renderitzar_trac_individual(self.ventana, trac["punts"], trac["color"], trac["gruix"])
        else:
            for p in self.model.particules:
                pygame.draw.circle(self.ventana, p["color"], (int(p["x"]), int(p["y"])), p["radi"])

            tots_punts = [p for t in tots_tracos for p in t["punts"]]
            min_x = min(p[0] for p in tots_punts)
            max_x = max(p[0] for p in tots_punts)
            min_y = min(p[1] for p in tots_punts)
            max_y = max(p[1] for p in tots_punts)

            centre_dibuix_x = (min_x + max_x) / 2.0
            alçada_total = max(1, max_y - min_y)

            t = self.model.temps_animacio
            tipus = self.model.tipus_animacio_detectat

            noms_efectes = {
                "onades": "Efecte Onades del Mar detectat!",
                "caminar": "Efecte Anar i Tornar (rebot als cantons)!",
                "ma": "Efecte Mà Detectat! Moviment de dits saludant!",
                "lletra": "Efecte A-Z / 0-9 Caminants! Ulls, boca, braços i cames!",
                "figura": "Efecte Figures Geomètriques Caminants! Ulls, boca, braços i cames!",
                "botar": "Efecte Saltar / Botar Alegre detectat!"
            }
            txt_efecte = self.font_estat.render(noms_efectes.get(tipus, ""), True, (120, 50, 160))
            self.ventana.blit(txt_efecte, (w // 2 - txt_efecte.get_width() // 2, 25))

            if tipus in ("lletra", "figura"):
                dx = self.model.x_transllacio
                grups = self.model.grups_personatges or [tots_tracos]

                for idx, grup_tracos in enumerate(grups):
                    punts_grup = [p for tr in grup_tracos for p in tr["punts"]]
                    if not punts_grup:
                        continue

                    g_min_x = min(p[0] for p in punts_grup)
                    g_max_x = max(p[0] for p in punts_grup)
                    g_min_y = min(p[1] for p in punts_grup)
                    g_max_y = max(p[1] for p in punts_grup)

                    desfasament = idx * 0.55
                    rebot_y = -abs(math.sin(t * 8.5 + desfasament)) * 10.0

                    for trac in grup_tracos:
                        punts_elem = [
                            (int(px + dx), int(py + rebot_y))
                            for px, py in trac["punts"]
                        ]
                        self._renderitzar_trac_individual(self.ventana, punts_elem, trac["color"], trac["gruix"])

                    self._dibuixar_anatomia_personatge(
                        self.ventana,
                        g_min_x + dx,
                        g_max_x + dx,
                        g_min_y + rebot_y,
                        g_max_y + rebot_y,
                        t,
                        self.model.direccio_x,
                        desfasament
                    )
                return

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
        self.btn_animar.draw(self.ventana, self.font_botons, seleccionat=(self.model.animant and self.model.tipus_animacio_detectat not in ("lletra", "figura")))
        self.btn_personatge.draw(self.ventana, self.font_botons, seleccionat=(self.model.animant and self.model.tipus_animacio_detectat in ("lletra", "figura")))

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