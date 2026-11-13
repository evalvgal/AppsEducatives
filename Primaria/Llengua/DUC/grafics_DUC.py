"""
La Regla Pnemotècnica del DUC — Interfície gràfica i bucle principal amb Pygame.
Requeriments: pip install pygame
Executar: python grafics_DUC.py
"""

import sys
import pygame
from DUC import DUCModel, COLOR_TEXTO, COLOR_CENTENA, COLOR_DECENA, COLOR_UNIDAD

# ==========================================
# CONFIGURACIÓ ARQUITECTÒNICA I UX INFANTIL
# ==========================================
pygame.init()

# Resolució lògica de disseny
ANCHO_LOGICO, ALTO_LOGICO = 1200, 800

# ─────────────────────────────────────────────────────────────────
# PALETA DE COLORS IMPORTADA I CONSISTENT
# ─────────────────────────────────────────────────────────────────
COLOR_FONDO = (245, 242, 255)             # Fons lila clar molt suau (BG)
COLOR_PIZARRA = (255, 255, 255)           # Blanc pur per a l'interior de les pissarres

# Botons d'interacció i estats
COLOR_BOTON = (90, 160, 255)              # Blau de botó principal (BTN_MAIN)
COLOR_BOTON_HOVER = (60, 130, 230)        # Blau interactiu (BTN_HOVER)
COLOR_BOTON_VER = (150, 110, 230)         # Lila interactiu per al botó de revelar
COLOR_BOTON_VER_HOVER = (120, 80, 200)
COLOR_BOTON_DESACTIVADO = (200, 195, 215) # Gris clar per quan s'ha revelat tot

# Botó Sortir
COLOR_BOTON_SALIR = (220, 75, 85)
COLOR_BOTON_SALIR_HOVER = (190, 45, 55)


def iniciar_pantalla_completa() -> tuple[pygame.Surface, pygame.Rect]:
    """
    Detecta la resolució nativa del monitor, MacBook o Pissarra Digital,
    obre la finestra a pantalla completa i calcula l'àrea d'escalat proporcional.
    """
    info_pantalla = pygame.display.Info()
    w_real, h_real = info_pantalla.current_w, info_pantalla.current_h

    ventana = pygame.display.set_mode((w_real, h_real), pygame.FULLSCREEN)
    pygame.display.set_caption("La Regla Pnemotècnica del DUC! 🦆")

    escala = min(w_real / ANCHO_LOGICO, h_real / ALTO_LOGICO)
    nou_w = int(ANCHO_LOGICO * escala)
    nou_h = int(ALTO_LOGICO * escala)

    offset_x = (w_real - nou_w) // 2
    offset_y = (h_real - nou_h) // 2

    area_render = pygame.Rect(offset_x, offset_y, nou_w, nou_h)
    return ventana, area_render


ventana, area_render = iniciar_pantalla_completa()
pantalla = pygame.Surface((ANCHO_LOGICO, ALTO_LOGICO))

# Fonts
fuente_titol = pygame.font.SysFont("Helvetica", 38, bold=True)
fuente_lletres = pygame.font.SysFont("Helvetica", 38, bold=True)
fuente_mnemo = pygame.font.SysFont("Helvetica", 140, bold=True)
fuente_gigante = pygame.font.SysFont("Helvetica", 90, bold=True)
fuente_media = pygame.font.SysFont("Helvetica", 28, bold=True)
fuente_peque = pygame.font.SysFont("Helvetica", 20, bold=True)
fuente_boton = pygame.font.SysFont("Helvetica", 24, bold=True)
fuente_salir = pygame.font.SysFont("Helvetica", 18, bold=True)

reloj = pygame.time.Clock()


class AplicacionDUCGrafica:
    def __init__(self) -> None:
        self.model = DUCModel()
        self.pantalla_completa = True
        self.columnas_x = [70, 440, 810]
        self.ancho_col, self.alto_pizarra, self.y_pizarra = 320, 310, 360
        
        # Botó Sortir a la part superior dreta (alineat amb el marge dret de la columna C: 810 + 320 = 1130)
        self.rect_boton_salir = pygame.Rect(ANCHO_LOGICO - 190, 18, 120, 44)

        self.rect_boton_cambiar = pygame.Rect(ANCHO_LOGICO // 2 - 310, ALTO_LOGICO - 90, 290, 60)
        self.rect_boton_ver = pygame.Rect(ANCHO_LOGICO // 2 + 20, ALTO_LOGICO - 90, 290, 60)

    def _recalcular_area(self) -> None:
        """Recalcula l'àrea de dibuix si es canvia entre pantalla completa i finestra."""
        global area_render
        w_real, h_real = ventana.get_size()
        escala = min(w_real / ANCHO_LOGICO, h_real / ALTO_LOGICO)
        nou_w = int(ANCHO_LOGICO * escala)
        nou_h = int(ALTO_LOGICO * escala)
        offset_x = (w_real - nou_w) // 2
        offset_y = (h_real - nou_h) // 2
        area_render = pygame.Rect(offset_x, offset_y, nou_w, nou_h)

    def alternar_pantalla_completa(self) -> None:
        """Permet commutar entre pantalla completa i finestra amb F11."""
        global ventana
        self.pantalla_completa = not self.pantalla_completa
        if self.pantalla_completa:
            info = pygame.display.Info()
            ventana = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
        else:
            ventana = pygame.display.set_mode((ANCHO_LOGICO, ALTO_LOGICO), pygame.RESIZABLE)
        self._recalcular_area()

    def obtener_pos_raton_logica(self) -> tuple[int, int]:
        """Tradueix les coordenades reals (ratolí o dit a la pissarra) a les lògiques (1200x800)."""
        pos_real = pygame.mouse.get_pos()
        if area_render.width <= 0 or area_render.height <= 0:
            return (0, 0)
        x = int((pos_real[0] - area_render.x) * (ANCHO_LOGICO / area_render.width))
        y = int((pos_real[1] - area_render.y) * (ALTO_LOGICO / area_render.height))
        return (x, y)

    def procesar_eventos(self) -> bool:
        pos_raton = self.obtener_pos_raton_logica()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            if evento.type == pygame.VIDEORESIZE and not self.pantalla_completa:
                self._recalcular_area()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.rect_boton_salir.collidepoint(pos_raton):
                    return False
                elif self.rect_boton_cambiar.collidepoint(pos_raton):
                    self.model.generar_nuevo_numero()
                elif self.rect_boton_ver.collidepoint(pos_raton):
                    self.model.avanzar_estado()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                elif evento.key == pygame.K_F11:
                    self.alternar_pantalla_completa()
                elif evento.key == pygame.K_SPACE or evento.key == pygame.K_RETURN:
                    self.model.avanzar_estado()
                elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_n:
                    self.model.generar_nuevo_numero()

        return True

    def renderizar_texto_multicolor(self, superficie, parts, y_pos) -> None:
        amplada_total = 0
        superficies_renderitzades = []
        
        cometa_ini = fuente_lletres.render("« ", True, COLOR_TEXTO)
        cometa_fi = fuente_lletres.render(" »", True, COLOR_TEXTO)
        
        amplada_total += cometa_ini.get_width()
        for text, color in parts:
            txt_surface = fuente_lletres.render(text, True, color)
            superficies_renderitzades.append(txt_surface)
            amplada_total += txt_surface.get_width()
        amplada_total += cometa_fi.get_width()
        
        x_actual = (ANCHO_LOGICO - amplada_total) // 2
        superficie.blit(cometa_ini, (x_actual, y_pos))
        x_actual += cometa_ini.get_width()
        
        for surf in superficies_renderitzades:
            superficie.blit(surf, (x_actual, y_pos))
            x_actual += surf.get_width()
            
        superficie.blit(cometa_fi, (x_actual, y_pos))

    def renderizar(self) -> None:
        pantalla.fill(COLOR_FONDO)
        pos_raton = self.obtener_pos_raton_logica()
        
        # Títol alineat a l'esquerra amb la columna D per deixar espai al botó Sortir a la dreta
        txt_titol = fuente_titol.render("Aprenem l'estructura dels nombres amb el DUC!", True, COLOR_TEXTO)
        pantalla.blit(txt_titol, (70, 20))

        # Botó Sortir a la cantonada superior dreta
        color_salir = COLOR_BOTON_SALIR_HOVER if self.rect_boton_salir.collidepoint(pos_raton) else COLOR_BOTON_SALIR
        pygame.draw.rect(pantalla, color_salir, self.rect_boton_salir, border_radius=12)
        pygame.draw.rect(pantalla, COLOR_TEXTO, self.rect_boton_salir, 2, border_radius=12)
        txt_btn_s = fuente_salir.render("Sortir ✕", True, COLOR_PIZARRA)
        pantalla.blit(txt_btn_s, txt_btn_s.get_rect(center=self.rect_boton_salir.center))
        
        txt_num_gran = fuente_gigante.render(str(self.model.numero_actual), True, COLOR_TEXTO)
        pantalla.blit(txt_num_gran, (ANCHO_LOGICO // 2 - txt_num_gran.get_width() // 2, 75))
        
        if self.model.estado_juego == 2:
            self.renderizar_texto_multicolor(pantalla, self.model.parts_text, 175)
        else:
            txt_incognita = fuente_lletres.render("« ???-???-??? »", True, (160, 150, 190))
            pantalla.blit(txt_incognita, (ANCHO_LOGICO // 2 - txt_incognita.get_width() // 2, 175))

        estructures = [
            ("D", "DESENES", COLOR_DECENA, self.columnas_x[0], str(self.model.decenas)),
            ("U", "UNITATS", COLOR_UNIDAD, self.columnas_x[1], str(self.model.unidades)),
            ("C", "CENTENES", COLOR_CENTENA, self.columnas_x[2], str(self.model.centenas))
        ]

        for lletra, nom_col, color, col_x, xifra in estructures:
            centro_columna = col_x + (self.ancho_col // 2)
            
            txt_lletra_duc = fuente_mnemo.render(lletra, True, color)
            pantalla.blit(txt_lletra_duc, (centro_columna - txt_lletra_duc.get_width() // 2, 225))
            
            pygame.draw.rect(pantalla, COLOR_PIZARRA, (col_x, self.y_pizarra, self.ancho_col, self.alto_pizarra), border_radius=20)
            pygame.draw.rect(pantalla, color, (col_x, self.y_pizarra, self.ancho_col, self.alto_pizarra), 4, border_radius=20)
            
            txt_nom = fuente_media.render(nom_col, True, color)
            pantalla.blit(txt_nom, (centro_columna - txt_nom.get_width() // 2, self.y_pizarra + 25))
            
            if self.model.estado_juego >= 1:
                txt_xifra = fuente_gigante.render(xifra, True, color)
                txt_equivalencia = fuente_peque.render(f"Valor: {int(xifra) * (10 if lletra=='D' else 1 if lletra=='U' else 100)} unitats", True, COLOR_TEXTO)
            else:
                txt_xifra = fuente_gigante.render("?", True, (200, 195, 215))
                txt_equivalencia = fuente_peque.render("Valor: ?? unitats", True, (170, 165, 185))
                
            pantalla.blit(txt_xifra, (centro_columna - txt_xifra.get_width() // 2, self.y_pizarra + 90))
            pantalla.blit(txt_equivalencia, (centro_columna - txt_equivalencia.get_width() // 2, self.y_pizarra + 230))

        color_cambiar = COLOR_BOTON_HOVER if self.rect_boton_cambiar.collidepoint(pos_raton) else COLOR_BOTON
        pygame.draw.rect(pantalla, color_cambiar, self.rect_boton_cambiar, border_radius=15)
        pygame.draw.rect(pantalla, COLOR_TEXTO, self.rect_boton_cambiar, 2, border_radius=15)
        txt_btn_c = fuente_boton.render("¡Canviar Número!", True, COLOR_PIZARRA)
        pantalla.blit(txt_btn_c, txt_btn_c.get_rect(center=self.rect_boton_cambiar.center))

        if self.model.estado_juego == 0:
            color_ver = COLOR_BOTON_VER_HOVER if self.rect_boton_ver.collidepoint(pos_raton) else COLOR_BOTON_VER
            texto_boton = "Veure el DUC"
        elif self.model.estado_juego == 1:
            color_ver = COLOR_BOTON_HOVER if self.rect_boton_ver.collidepoint(pos_raton) else COLOR_BOTON
            texto_boton = "Veure com s'escriu"
        else:
            color_ver = COLOR_BOTON_DESACTIVADO
            texto_boton = "Tot descobert!"

        pygame.draw.rect(pantalla, color_ver, self.rect_boton_ver, border_radius=15)
        pygame.draw.rect(pantalla, COLOR_TEXTO, self.rect_boton_ver, 2, border_radius=15)
        txt_btn_v = fuente_boton.render(texto_boton, True, COLOR_TEXTO if self.model.estado_juego == 2 else COLOR_PIZARRA)
        pantalla.blit(txt_btn_v, txt_btn_v.get_rect(center=self.rect_boton_ver.center))

        ventana.fill(COLOR_FONDO)
        superficie_escalada = pygame.transform.smoothscale(pantalla, (area_render.width, area_render.height))
        ventana.blit(superficie_escalada, area_render.topleft)
        pygame.display.flip()


def main() -> None:
    app = AplicacionDUCGrafica()
    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        ejecutando = app.procesar_eventos()
        app.renderizar()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()