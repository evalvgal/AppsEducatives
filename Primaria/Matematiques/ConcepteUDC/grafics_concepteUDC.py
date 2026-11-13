"""
Concepte UDC — Interfície gràfica i bucle principal amb Pygame.
Requeriments: pip install pygame
Executar: python grafics_concepteUDC.py
"""

import sys
import pygame
from concepteUDC import ConcepteUDCModel

# ==========================================
# CONFIGURACIÓ ARQUITECTÒNICA I UX INFANTIL
# ==========================================
pygame.init()

# Dimensions de la pantalla originals (resolució lògica)
ANCHO_LOGICO, ALTO_LOGICO = 1050, 680

# ─────────────────────────────────────────────────────────────────
# PALETA DE COLORS IMPORTADA I ADAPTADA DE "SUMA AMB PORTADES"
# ─────────────────────────────────────────────────────────────────
COLOR_FONDO = (245, 242, 255)       # Fons lila clar molt suau (BG)
COLOR_PIZARRA = (255, 255, 255)     # Blanc pur per a l'interior de les pissarres
COLOR_TEXTO = (50, 40, 80)          # Lila fosc per a textos llegibles (TEXT_DARK)

# Colors estructurals i de blocs (Centenes, Desenes, Unitats)
COLOR_CENTENA = (230, 170, 120)     # Préssec / Marró suau (C_COL_BD)
COLOR_DECENA = (120, 170, 230)      # Blau cel educatiu (D_COL_BD)
COLOR_UNIDAD = (100, 210, 140)      # Verd menta (U_COL_BD)

# Botons interactius
COLOR_BOTON = (90, 160, 255)        # Blau de botó principal (BTN_MAIN)
COLOR_BOTON_HOVER = (60, 130, 230)  # Blau interactiu actiu (BTN_HOVER)

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
    pygame.display.set_caption("¡Aprenem les Centenes, Desenes i Unitats! 🧮")

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
fuente_gigante = pygame.font.SysFont("Helvetica", 65, bold=True)
fuente_grande = pygame.font.SysFont("Helvetica", 40, bold=True)
fuente_media = pygame.font.SysFont("Helvetica", 24, bold=True)
fuente_peque = pygame.font.SysFont("Helvetica", 18, bold=True)
fuente_boton = pygame.font.SysFont("Helvetica", 32, bold=True)
fuente_salir = pygame.font.SysFont("Helvetica", 18, bold=True)

reloj = pygame.time.Clock()


class BloqueBase10:
    @staticmethod
    def dibujar_cubito(superficie, x, y, tam, color):
        pygame.draw.rect(superficie, color, (x, y, tam, tam), border_radius=1)
        pygame.draw.rect(superficie, (255, 255, 255), (x, y, tam, tam), 1, border_radius=1)
        pygame.draw.rect(superficie, COLOR_TEXTO, (x, y, tam, tam), 1, border_radius=1)

    @classmethod
    def dibujar_centena(cls, superficie, x, y):
        tam_cubo = 7  
        for fila in range(10):
            for col in range(10):
                cls.dibujar_cubito(superficie, x + (col * tam_cubo), y + (fila * tam_cubo), tam_cubo, COLOR_CENTENA)

    @classmethod
    def dibujar_decena(cls, superficie, x, y):
        tam_cubo = 15
        for fila in range(10):
            cls.dibujar_cubito(superficie, x, y + (fila * tam_cubo), tam_cubo, COLOR_DECENA)

    @classmethod
    def dibujar_unidad(cls, superficie, x, y):
        cls.dibujar_cubito(superficie, x, y, 22, COLOR_UNIDAD)


class AplicacionEducativaGrafica:
    def __init__(self) -> None:
        self.model = ConcepteUDCModel()
        self.pantalla_completa = True
        self.columnas_x = [60, 385, 710]
        self.ancho_col, self.alto_pizarra, self.y_pizarra = 280, 380, 190
        
        # Botó Sortir a la part superior dreta (alineat amb el marge dret de la columna Unitats: 710 + 280 = 990)
        self.rect_boton_salir = pygame.Rect(ANCHO_LOGICO - 180, 15, 120, 42)
        
        self.rect_boton = pygame.Rect(ANCHO_LOGICO // 2 - 150, ALTO_LOGICO - 80, 300, 60)

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
        """Tradueix les coordenades reals (ratolí o dit a la pissarra) a les lògiques (1050x680)."""
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
                elif self.rect_boton.collidepoint(pos_raton):
                    self.model.generar_nuevo_numero()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                elif evento.key == pygame.K_F11:
                    self.alternar_pantalla_completa()
                elif evento.key == pygame.K_SPACE or evento.key == pygame.K_RETURN or evento.key == pygame.K_RIGHT:
                    self.model.generar_nuevo_numero()

        return True

    def renderizar(self) -> None:
        pantalla.fill(COLOR_FONDO)
        pos_raton = self.obtener_pos_raton_logica()

        # Instrucció superior alineada a l'esquerra amb la columna Centenes per deixar espai al botó Sortir
        txt_instrucciones = fuente_media.render("¡Mira el número i compta els blocs màgics!", True, COLOR_TEXTO)
        pantalla.blit(txt_instrucciones, (60, 22))

        # Botó Sortir a la cantonada superior dreta
        color_salir = COLOR_BOTON_SALIR_HOVER if self.rect_boton_salir.collidepoint(pos_raton) else COLOR_BOTON_SALIR
        pygame.draw.rect(pantalla, color_salir, self.rect_boton_salir, border_radius=12)
        pygame.draw.rect(pantalla, COLOR_TEXTO, self.rect_boton_salir, 2, border_radius=12)
        txt_btn_s = fuente_salir.render("Sortir", True, COLOR_PIZARRA)
        pantalla.blit(txt_btn_s, txt_btn_s.get_rect(center=self.rect_boton_salir.center))

        cifras = [
            (str(self.model.centenas), "Centenes", COLOR_CENTENA, self.columnas_x[0]),
            (str(self.model.decenas), "Desenes", COLOR_DECENA, self.columnas_x[1]),
            (str(self.model.unidades), "Unitats", COLOR_UNIDAD, self.columnas_x[2])
        ]

        for valor, etiqueta, color, col_x in cifras:
            centro_columna = col_x + (self.ancho_col // 2)
            txt_num = fuente_gigante.render(valor, True, color)
            pantalla.blit(txt_num, (centro_columna - txt_num.get_width() // 2, 65))
            txt_lbl = fuente_media.render(etiqueta, True, color)
            pantalla.blit(txt_lbl, (centro_columna - txt_lbl.get_width() // 2, 135))

        for i, (nombre, color) in enumerate([
            ("CENTENES (100)", COLOR_CENTENA),
            ("DESENES (10)", COLOR_DECENA),
            ("UNITATS (1)", COLOR_UNIDAD)
        ]):
            x_col = self.columnas_x[i]
            pygame.draw.rect(pantalla, COLOR_PIZARRA, (x_col, self.y_pizarra, self.ancho_col, self.alto_pizarra), border_radius=15)
            pygame.draw.rect(pantalla, color, (x_col, self.y_pizarra, self.ancho_col, self.alto_pizarra), 3, border_radius=15)
            txt_col = fuente_peque.render(nombre, True, color)
            pantalla.blit(txt_col, (x_col + self.ancho_col // 2 - txt_col.get_width() // 2, self.y_pizarra + 15))

        # Dibuix de blocs
        for c in range(self.model.centenas):
            fila_c, col_c = c // 3, c % 3
            BloqueBase10.dibujar_centena(pantalla, self.columnas_x[0] + 25 + (col_c * 80), self.y_pizarra + 65 + (fila_c * 80))
        for d in range(self.model.decenas):
            BloqueBase10.dibujar_decena(pantalla, self.columnas_x[1] + 20 + (d * 26), self.y_pizarra + 90)
        for u in range(self.model.unidades):
            fila_u, col_u = u // 3, u % 3
            BloqueBase10.dibujar_unidad(pantalla, self.columnas_x[2] + 45 + (col_u * 70), self.y_pizarra + 80 + (fila_u * 75))

        color_btn = COLOR_BOTON_HOVER if self.rect_boton.collidepoint(pos_raton) else COLOR_BOTON
        pygame.draw.rect(pantalla, color_btn, self.rect_boton, border_radius=14)
        pygame.draw.rect(pantalla, COLOR_TEXTO, self.rect_boton, 2, border_radius=14)
        
        txt_btn = fuente_boton.render("¡Canviar Número!", True, (255, 255, 255))
        txt_rect = txt_btn.get_rect(center=self.rect_boton.center)
        pantalla.blit(txt_btn, txt_rect)

        ventana.fill(COLOR_FONDO)
        superficie_escalada = pygame.transform.smoothscale(pantalla, (area_render.width, area_render.height))
        ventana.blit(superficie_escalada, area_render.topleft)
        pygame.display.flip()


def main() -> None:
    app = AplicacionEducativaGrafica()
    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        ejecutando = app.procesar_eventos()
        app.renderizar()
    pygame.quit()
    sys.exit()


if __name__ == "__main__": 
    main()