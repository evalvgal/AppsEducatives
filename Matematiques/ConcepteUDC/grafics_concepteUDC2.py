"""
Concepte UDC 2 — Interfície gràfica i bucle principal amb Pygame.
Requeriments: pip install pygame
Executar: python grafics_concepteUDC2.py
"""

import sys
import pygame
from concepteUDC2 import ConcepteUDC2Model

# ==========================================
# CONFIGURACIÓ ARQUITECTÒNICA I UX INFANTIL
# ==========================================
pygame.init()

# Resolució lògica de disseny
ANCHO_LOGICO, ALTO_LOGICO = 1200, 800

# Obtenim informació de la pantalla del dispositiu actual
info_pantalla = pygame.display.Info()
ancho_pantalla_disponible = info_pantalla.current_w
alto_pantalla_disponible = info_pantalla.current_h

# Calculem una mida de finestra adaptada a pantalles més petites (p.ex. portàtils Windows)
ancho_ventana = min(ANCHO_LOGICO, int(ancho_pantalla_disponible * 0.85))
alto_ventana = min(ALTO_LOGICO, int(alto_pantalla_disponible * 0.80))

# Assegurar proporció
proporcion = ANCHO_LOGICO / ALTO_LOGICO
if ancho_ventana / alto_ventana > proporcion:
    ancho_ventana = int(alto_ventana * proporcion)
else:
    alto_ventana = int(ancho_ventana / proporcion)

# Finestra real redimensionable i pantalla virtual de dibuix
ventana = pygame.display.set_mode((ancho_ventana, alto_ventana), pygame.RESIZABLE)
pantalla = pygame.Surface((ANCHO_LOGICO, ALTO_LOGICO))

pygame.display.set_caption("¡Aprenem les Centenes, Desenes i Unitats! 🧮")

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

# Botons i caixes d'explicació
COLOR_BOTON = (90, 160, 255)        # Blau de botó principal (BTN_MAIN)
COLOR_BOTON_HOVER = (60, 130, 230)  # Blau interactiu (BTN_HOVER)
COLOR_EXPLICACION = (255, 255, 255) # Fons net per al resum pedagògic

# Fonts
fuente_gigante = pygame.font.SysFont("Helvetica", 70, bold=True)
fuente_grande = pygame.font.SysFont("Helvetica", 45, bold=True)
fuente_media = pygame.font.SysFont("Helvetica", 26, bold=True)
fuente_explicacion = pygame.font.SysFont("Helvetica", 22, bold=False)
fuente_explicacion_bold = pygame.font.SysFont("Helvetica", 22, bold=True)
fuente_peque = pygame.font.SysFont("Helvetica", 18, bold=True)
fuente_boton = pygame.font.SysFont("Helvetica", 32, bold=True)

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

class AplicacionEducativaGrafica2:
    def __init__(self) -> None:
        self.model = ConcepteUDC2Model()
        self.columnas_x = [70, 440, 810]
        self.ancho_col, self.alto_pizarra, self.y_pizarra = 320, 360, 190
        self.rect_boton = pygame.Rect(ANCHO_LOGICO // 2 - 150, ALTO_LOGICO - 85, 300, 60)

    def obtener_pos_raton_logica(self) -> tuple[int, int]:
        pos_real = pygame.mouse.get_pos()
        w_real, h_real = ventana.get_size()
        x = int(pos_real[0] * (ANCHO_LOGICO / w_real)) if w_real > 0 else 0
        y = int(pos_real[1] * (ALTO_LOGICO / h_real)) if h_real > 0 else 0
        return (x, y)

    def procesar_eventos(self) -> bool:
        pos_raton = self.obtener_pos_raton_logica()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.rect_boton.collidepoint(pos_raton):
                    self.model.generar_nuevo_numero()
        return True

    def renderizar_texto_mixto(self, superficie, partes, x, y) -> None:
        x_actual = x
        for texto, es_bold, color in partes:
            fuente = fuente_explicacion_bold if es_bold else fuente_explicacion
            render = fuente.render(texto, True, color)
            superficie.blit(render, (x_actual, y))
            x_actual += render.get_width()

    def renderizar(self) -> None:
        pantalla.fill(COLOR_FONDO)
        txt_instrucciones = fuente_media.render("¡Mira el número i compta els blocs màgics!", True, COLOR_TEXTO)
        pantalla.blit(txt_instrucciones, (ANCHO_LOGICO // 2 - txt_instrucciones.get_width() // 2, 20))

        cifras = [
            (str(self.model.centenas), "Centenes", COLOR_CENTENA, self.columnas_x[0]),
            (str(self.model.decenas), "Desenes", COLOR_DECENA, self.columnas_x[1]),
            (str(self.model.unidades), "Unitats", COLOR_UNIDAD, self.columnas_x[2])
        ]

        for valor, etiqueta, color, col_x in cifras:
            centro_columna = col_x + (self.ancho_col // 2)
            txt_num = fuente_gigante.render(valor, True, color)
            pantalla.blit(txt_num, (centro_columna - txt_num.get_width() // 2, 60))
            txt_lbl = fuente_media.render(etiqueta, True, color)
            pantalla.blit(txt_lbl, (centro_columna - txt_lbl.get_width() // 2, 130))

        for i, (nombre, color) in enumerate([
            ("CENTENARS (100)", COLOR_CENTENA),
            ("DESENES (10)", COLOR_DECENA),
            ("UNITATS (1)", COLOR_UNIDAD)
        ]):
            x_col = self.columnas_x[i]
            pygame.draw.rect(pantalla, COLOR_PIZARRA, (x_col, self.y_pizarra, self.ancho_col, self.alto_pizarra), border_radius=15)
            pygame.draw.rect(pantalla, color, (x_col, self.y_pizarra, self.ancho_col, self.alto_pizarra), 4, border_radius=15)
            txt_col = fuente_peque.render(nombre, True, color)
            pantalla.blit(txt_col, (x_col + self.ancho_col // 2 - txt_col.get_width() // 2, self.y_pizarra + 15))

        # Dibuix de blocs adaptats
        for c in range(self.model.centenas):
            fila_c, col_c = c // 3, c % 3
            BloqueBase10.dibujar_centena(pantalla, self.columnas_x[0] + 45 + (col_c * 85), self.y_pizarra + 65 + (fila_c * 85))
        for d in range(self.model.decenas):
            BloqueBase10.dibujar_decena(pantalla, self.columnas_x[1] + 35 + (d * 27), self.y_pizarra + 90)
        for u in range(self.model.unidades):
            fila_u, col_u = u // 4, u % 4
            BloqueBase10.dibujar_unidad(pantalla, self.columnas_x[2] + 45 + (col_u * 60), self.y_pizarra + 80 + (fila_u * 70))

        # ==========================================
        # SECCIÓ PEDAGÒGICA INTEGRADA (NOUS COLORS)
        # ==========================================
        y_box = 570
        rect_explicacion = pygame.Rect(70, y_box, ANCHO_LOGICO - 140, 120)
        pygame.draw.rect(pantalla, COLOR_PIZARRA, rect_explicacion, border_radius=15)
        pygame.draw.rect(pantalla, (110, 100, 140), rect_explicacion, 2, border_radius=15)

        # Plurals/Singulars en català
        str_centena = "centena" if self.model.centenas == 1 else "centenes"
        str_decena = "desena" if self.model.decenas == 1 else "desenes"
        str_unidad = "unitat" if self.model.unidades == 1 else "unitats"

        # Línia 1: Desglossament amb èmfasi cromàtic idèntic
        partes_l1 = [
            ("El número ", False, COLOR_TEXTO),
            (f"{self.model.numero_actual}", True, COLOR_TEXTO),
            (" té: ", False, COLOR_TEXTO),
            (f"{self.model.centenas} ", True, COLOR_CENTENA),
            (f"{str_centena}, ", False, COLOR_TEXTO),
            (f"{self.model.decenas} ", True, COLOR_DECENA),
            (f"{str_decena} i ", False, COLOR_TEXTO),
            (f"{self.model.unidades} ", True, COLOR_UNIDAD),
            (f"{str_unidad}.", False, COLOR_TEXTO)
        ]
        
        # Línia 2: Equivalències de les centenes
        partes_l2 = [
            ("• Les ", False, COLOR_TEXTO),
            (f"{self.model.centenas} ", True, COLOR_CENTENA),
            (f"{str_centena} equivalen a: ", False, COLOR_TEXTO),
            (f"{self.model.centenas * 10} ", True, COLOR_DECENA),
            ("desenes o a ", False, COLOR_TEXTO),
            (f"{self.model.centenas * 100} ", True, COLOR_UNIDAD),
            ("unitats.", False, COLOR_TEXTO)
        ]

        # Línia 3: Equivalències de les desenes
        partes_l3 = [
            ("• Les ", False, COLOR_TEXTO),
            (f"{self.model.decenas} ", True, COLOR_DECENA),
            (f"{str_decena} equivalen a: ", False, COLOR_TEXTO),
            (f"{self.model.decenas * 10} ", True, COLOR_UNIDAD),
            ("unitats.", False, COLOR_TEXTO)
        ]

        # Renderitzar el text
        self.renderizar_texto_mixto(pantalla, partes_l1, rect_explicacion.x + 25, rect_explicacion.y + 15)
        self.renderizar_texto_mixto(pantalla, partes_l2, rect_explicacion.x + 25, rect_explicacion.y + 50)
        self.renderizar_texto_mixto(pantalla, partes_l3, rect_explicacion.x + 25, rect_explicacion.y + 80)

        # --- SECCIÓ DEL BOTÓ ---
        pos_raton = self.obtener_pos_raton_logica()
        color_btn = COLOR_BOTON_HOVER if self.rect_boton.collidepoint(pos_raton) else COLOR_BOTON
        pygame.draw.rect(pantalla, color_btn, self.rect_boton, border_radius=14)
        pygame.draw.rect(pantalla, COLOR_TEXTO, self.rect_boton, 2, border_radius=14)
        
        txt_btn = fuente_boton.render("¡Canviar Número!", True, (255, 255, 255))
        txt_rect = txt_btn.get_rect(center=self.rect_boton.center)
        pantalla.blit(txt_btn, txt_rect)

        # Reescalar la superfície virtual a la finestra real
        ventana.blit(pygame.transform.smoothscale(pantalla, ventana.get_size()), (0, 0))
        pygame.display.flip()

def main() -> None:
    app = AplicacionEducativaGrafica2()
    ejecutando = True
    while ejecutando:
        reloj.tick(60)
        ejecutando = app.procesar_eventos()
        app.renderizar()
    pygame.quit()
    sys.exit()

if __name__ == "__main__": 
    main()