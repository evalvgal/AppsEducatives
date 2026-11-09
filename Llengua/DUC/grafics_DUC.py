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

# Resolució lògica de disseny (la que funciona perfectament)
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

pygame.display.set_caption("La Regla Pnemotècnica del DUC! 🦆")

# ─────────────────────────────────────────────────────────────────
# PALETA DE COLORS IMPORTADA I CONSISTENT
# ─────────────────────────────────────────────────────────────────
COLOR_FONDO = (245, 242, 255)       # Fons lila clar molt suau (BG)
COLOR_PIZARRA = (255, 255, 255)     # Blanc pur per a l'interior de les pissarres

# Botons d'interacció i estats
COLOR_BOTON = (90, 160, 255)        # Blau de botó principal (BTN_MAIN)
COLOR_BOTON_HOVER = (60, 130, 230)  # Blau interactiu (BTN_HOVER)
COLOR_BOTON_VER = (150, 110, 230)   # Lila interactiu per al botó de revelar
COLOR_BOTON_VER_HOVER = (120, 80, 200)
COLOR_BOTON_DESACTIVADO = (200, 195, 215) # Gris clar per quan s'ha revelat tot

# Fonts
fuente_titol = pygame.font.SysFont("Helvetica", 42, bold=True)
fuente_lletres = pygame.font.SysFont("Helvetica", 38, bold=True)
fuente_mnemo = pygame.font.SysFont("Helvetica", 140, bold=True)
fuente_gigante = pygame.font.SysFont("Helvetica", 90, bold=True)
fuente_media = pygame.font.SysFont("Helvetica", 28, bold=True)
fuente_peque = pygame.font.SysFont("Helvetica", 20, bold=True)
fuente_boton = pygame.font.SysFont("Helvetica", 24, bold=True)

reloj = pygame.time.Clock()


class AplicacionDUCGrafica:
    def __init__(self) -> None:
        self.model = DUCModel()
        self.columnas_x = [70, 440, 810]
        self.ancho_col, self.alto_pizarra, self.y_pizarra = 320, 310, 360
        
        self.rect_boton_cambiar = pygame.Rect(ANCHO_LOGICO // 2 - 310, ALTO_LOGICO - 90, 290, 60)
        self.rect_boton_ver = pygame.Rect(ANCHO_LOGICO // 2 + 20, ALTO_LOGICO - 90, 290, 60)

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
                if self.rect_boton_cambiar.collidepoint(pos_raton):
                    self.model.generar_nuevo_numero()
                elif self.rect_boton_ver.collidepoint(pos_raton):
                    self.model.avanzar_estado()
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
        
        txt_titol = fuente_titol.render("Aprenem l'estructura dels nombres amb el DUC!", True, COLOR_TEXTO)
        pantalla.blit(txt_titol, (ANCHO_LOGICO // 2 - txt_titol.get_width() // 2, 20))
        
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

        ventana.blit(pygame.transform.smoothscale(pantalla, ventana.get_size()), (0, 0))
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