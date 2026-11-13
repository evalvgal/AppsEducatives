import pygame
import random
import math

class VistaLectoEscriptura:
    def __init__(self, amplada=1280, alcada=720):
        pygame.init()
        self.amplada = amplada
        self.alcada = alcada
        self.pantalla = pygame.display.set_mode((self.amplada, self.alcada))
        pygame.display.set_caption("Aprèn a escriure - Pissarra Digital")
        
        self.rellotge = pygame.time.Clock()
        
        # Colors (Paleta infantil i accessible)
        self.BLANC = (255, 255, 255)
        self.BLAU_Fons = (240, 248, 255)
        self.GRIS_Guia = (210, 215, 220)
        self.VERMELL_Traç = (231, 76, 60)
        self.VERD_Exit = (46, 204, 113)
        self.BLAU_Botó = (52, 152, 219)
        self.Taronja_Opcio = (243, 156, 18)
        self.TEXT_Color = (44, 62, 80)
        
        # Fonts
        try:
            self.font_gran = pygame.font.SysFont("Arial", 350, bold=True)
            self.font_mitjana = pygame.font.SysFont("Arial", 40, bold=True)
            self.font_petita = pygame.font.SysFont("Arial", 28)
        except:
            self.font_gran = pygame.font.Font(None, 400)
            self.font_mitjana = pygame.font.SysFont(None, 50)
            self.font_petita = pygame.font.SysFont(None, 30)

        # Partícules de confeti
        self.confeti = []

    def dibuixar_fons(self, missatge=""):
        self.pantalla.fill(self.BLAU_Fons)
        if missatge:
            txt = self.font_mitjana.render(missatge, True, self.TEXT_Color)
            rect_txt = txt.get_rect(center=(self.amplada // 2, 50))
            self.pantalla.blit(txt, rect_txt)

    def obtenir_rect_sortir(self):
        return pygame.Rect(self.amplada - 140, 20, 120, 50)

    def dibuixar_boto_sortir(self):
        boto_sortir_rect = self.obtenir_rect_sortir()
        pygame.draw.rect(self.pantalla, self.VERMELL_Traç, boto_sortir_rect, border_radius=12)
        txt_sortir = self.font_petita.render("Sortir", True, self.BLANC)
        self.pantalla.blit(txt_sortir, txt_sortir.get_rect(center=boto_sortir_rect.center))
        return boto_sortir_rect

    def dibuixar_menu_principal(self):
        boto_nombres_rect = pygame.Rect(self.amplada // 2 - 350, self.alcada // 2 - 60, 300, 150)
        boto_lletres_rect = pygame.Rect(self.amplada // 2 + 50, self.alcada // 2 - 60, 300, 150)

        pygame.draw.rect(self.pantalla, self.BLAU_Botó, boto_nombres_rect, border_radius=20)
        pygame.draw.rect(self.pantalla, self.Taronja_Opcio, boto_lletres_rect, border_radius=20)

        txt_nombres = self.font_mitjana.render("NOMBRES", True, self.BLANC)
        txt_lletres = self.font_mitjana.render("LLETRES", True, self.BLANC)

        self.pantalla.blit(txt_nombres, txt_nombres.get_rect(center=boto_nombres_rect.center))
        self.pantalla.blit(txt_lletres, txt_lletres.get_rect(center=boto_lletres_rect.center))

        return boto_nombres_rect, boto_lletres_rect

    def dibuixar_menu_inicial(self):
        boto_maj_rect = pygame.Rect(self.amplada // 2 - 350, self.alcada // 2 - 60, 300, 150)
        boto_min_rect = pygame.Rect(self.amplada // 2 + 50, self.alcada // 2 - 60, 300, 150)

        pygame.draw.rect(self.pantalla, self.BLAU_Botó, boto_maj_rect, border_radius=20)
        pygame.draw.rect(self.pantalla, self.Taronja_Opcio, boto_min_rect, border_radius=20)

        txt_maj = self.font_mitjana.render("MAJÚSCULES", True, self.BLANC)
        txt_min = self.font_mitjana.render("minúscules", True, self.BLANC)

        self.pantalla.blit(txt_maj, txt_maj.get_rect(center=boto_maj_rect.center))
        self.pantalla.blit(txt_min, txt_min.get_rect(center=boto_min_rect.center))

        return boto_maj_rect, boto_min_rect

    def dibuixar_pantalla_entrada_element(self, element_actual, practica, tipus_lletra=""):
        if practica == "LLETRA":
            text_tipus = f"Tipus: {'MAJÚSCULES' if tipus_lletra == 'MAJUSCULA' else 'minúscules'}"
            instruccio = "Escriu una lletra al teclat i prem 'ENTER'"
        else:
            text_tipus = "Mode: NOMBRES (0 al 9)"
            instruccio = "Escriu un nombre al teclat i prem 'ENTER'"

        txt_t = self.font_petita.render(text_tipus, True, self.TEXT_Color)
        self.pantalla.blit(txt_t, (50, 100))

        display_elem = element_actual if element_actual else "_"
        txt_l = self.font_gran.render(display_elem, True, self.BLAU_Botó)
        rect_l = txt_l.get_rect(center=(self.amplada // 2, self.alcada // 2))
        self.pantalla.blit(txt_l, rect_l)

        txt_instruccions = self.font_mitjana.render(instruccio, True, self.TEXT_Color)
        rect_inst = txt_instruccions.get_rect(center=(self.amplada // 2, self.alcada - 100))
        self.pantalla.blit(txt_instruccions, rect_inst)

    def interpolar_linia(self, p1, p2, passos=25):
        punts = []
        for i in range(passos + 1):
            t = i / passos
            x = int(p1[0] + (p2[0] - p1[0]) * t)
            y = int(p1[1] + (p2[1] - p1[1]) * t)
            punts.append((x, y))
        return punts

    def generar_ruta_element(self, element, practica, tipus_lletra="MAJUSCULA"):
        cx, cy = self.amplada // 2, self.alcada // 2
        x_esq, x_dre = cx - 90, cx + 90
        y_dalt, y_baix = cy - 140, cy + 140
        y_mitj = cy

        ruta = []

        if practica == "LLETRA":
            lletra_up = element.upper()
            lletra_lower = element.lower()

            if tipus_lletra == "MAJUSCULA":
                if lletra_up == 'A':
                    ruta.extend(self.interpolar_linia((x_esq + 20, y_baix), (cx, y_dalt)))
                    ruta.extend(self.interpolar_linia((cx, y_dalt), (x_dre - 20, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq + 45, y_mitj + 20), (x_dre - 45, y_mitj + 20)))
                elif lletra_up == 'B':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_esq, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (cx + 20, y_dalt)))
                    for i in range(20):
                        a = math.pi/2 - math.pi * (i/19.0)
                        ruta.append((int(cx + 20 + 40 * math.cos(a)), int(cy - 70 + 40 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((cx + 20, y_mitj), (x_esq, y_mitj)))
                    for i in range(20):
                        a = math.pi/2 - math.pi * (i/19.0)
                        ruta.append((int(cx + 20 + 40 * math.cos(a)), int(cy + 70 + 40 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((cx + 20, y_baix), (x_esq, y_baix)))
                elif lletra_up == 'C':
                    for i in range(30):
                        a = math.pi/4 + (1.5 * math.pi) * (i/29.0)
                        ruta.append((int(cx + 30 + 70 * math.cos(a)), int(cy + 70 * math.sin(a))))
                elif lletra_up == 'D':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_esq, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (cx, y_dalt)))
                    for i in range(25):
                        a = math.pi/2 - math.pi * (i/24.0)
                        ruta.append((int(cx + 40 * math.cos(a)), int(cy + 140 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((cx, y_baix), (x_esq, y_baix)))
                elif lletra_up == 'E':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_esq, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_dre, y_dalt)))
                    ruta.extend(self.interpolar_linia((x_esq, y_mitj), (cx + 20, y_mitj)))
                    ruta.extend(self.interpolar_linia((x_esq, y_baix), (x_dre, y_baix)))
                elif lletra_up == 'F':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_esq, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_dre, y_dalt)))
                    ruta.extend(self.interpolar_linia((x_esq, y_mitj), (cx + 20, y_mitj)))
                elif lletra_up == 'G':
                    for i in range(25):
                        a = math.pi/4 + (1.6 * math.pi) * (i/24.0)
                        ruta.append((int(cx + 30 + 70 * math.cos(a)), int(cy + 70 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((x_dre - 10, cy), (x_dre, cy)))
                    ruta.extend(self.interpolar_linia((x_dre, cy), (x_dre, y_baix - 20)))
                elif lletra_up == 'H':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_esq, y_baix)))
                    ruta.extend(self.interpolar_linia((x_dre, y_dalt), (x_dre, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq, y_mitj), (x_dre, y_mitj)))
                elif lletra_up == 'I':
                    ruta.extend(self.interpolar_linia((cx, y_dalt), (cx, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq + 20, y_dalt), (x_dre - 20, y_dalt)))
                    ruta.extend(self.interpolar_linia((x_esq + 20, y_baix), (x_dre - 20, y_baix)))
                elif lletra_up == 'J':
                    ruta.extend(self.interpolar_linia((x_esq + 20, y_dalt), (x_dre, y_dalt)))
                    ruta.extend(self.interpolar_linia((cx + 20, y_dalt), (cx + 20, y_baix - 30)))
                    for i in range(15):
                        a = math.pi * (i/14.0)
                        ruta.append((int(cx + 20 - 30 * math.sin(a)), int(y_baix - 30 + 30 * (1 - math.cos(a)))))
                elif lletra_up == 'K':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_esq, y_baix)))
                    ruta.extend(self.interpolar_linia((x_dre, y_dalt), (x_esq, y_mitj)))
                    ruta.extend(self.interpolar_linia((x_esq, y_mitj), (x_dre, y_baix)))
                elif lletra_up == 'L':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_esq, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq, y_baix), (x_dre, y_baix)))
                elif lletra_up == 'M':
                    ruta.extend(self.interpolar_linia((x_esq, y_baix), (x_esq, y_dalt)))
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (cx, y_mitj)))
                    ruta.extend(self.interpolar_linia((cx, y_mitj), (x_dre, y_dalt)))
                    ruta.extend(self.interpolar_linia((x_dre, y_dalt), (x_dre, y_baix)))
                elif lletra_up == 'N':
                    ruta.extend(self.interpolar_linia((x_esq, y_baix), (x_esq, y_dalt)))
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_dre, y_baix)))
                    ruta.extend(self.interpolar_linia((x_dre, y_baix), (x_dre, y_dalt)))
                elif lletra_up == 'O':
                    for i in range(35):
                        a = 2 * math.pi * (i / 34.0)
                        ruta.append((int(cx + 70 * math.cos(a)), int(cy + 90 * math.sin(a))))
                elif lletra_up == 'P':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_esq, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_dre, y_dalt)))
                    ruta.extend(self.interpolar_linia((x_dre, y_dalt), (x_dre, y_mitj)))
                    ruta.extend(self.interpolar_linia((x_dre, y_mitj), (x_esq, y_mitj)))
                elif lletra_up == 'Q':
                    for i in range(35):
                        a = 2 * math.pi * (i / 34.0)
                        ruta.append((int(cx + 70 * math.cos(a)), int(cy + 90 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((cx, cy + 30), (x_dre, y_baix)))
                elif lletra_up == 'R':
                    ruta.extend(self.interpolar_linia((x_esq, y_baix), (x_esq, y_dalt)))
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_dre, y_dalt)))
                    ruta.extend(self.interpolar_linia((x_dre, y_dalt), (x_dre, y_mitj)))
                    ruta.extend(self.interpolar_linia((x_dre, y_mitj), (x_esq, y_mitj)))
                    ruta.extend(self.interpolar_linia((x_esq, y_mitj), (x_dre, y_baix)))
                elif lletra_up == 'S':
                    for i in range(25):
                        a = math.pi * (i / 24.0)
                        ruta.append((int(cx + 50 * math.cos(a + math.pi/2)), int(y_dalt + 50 + 50 * math.sin(a + math.pi/2))))
                    for i in range(25):
                        a = math.pi * (i / 24.0)
                        ruta.append((int(cx - 50 * math.cos(a + math.pi/2)), int(y_baix - 50 + 50 * math.sin(a + math.pi/2))))
                elif lletra_up == 'T':
                    ruta.extend(self.interpolar_linia((cx, y_dalt), (cx, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_dre, y_dalt)))
                elif lletra_up == 'U':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_esq, y_baix - 30)))
                    for i in range(15):
                        a = math.pi * (i / 14.0)
                        ruta.append((int(cx - 50 * math.cos(a)), int(y_baix - 30 + 30 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((x_dre, y_baix - 30), (x_dre, y_dalt)))
                elif lletra_up == 'V':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (cx, y_baix)))
                    ruta.extend(self.interpolar_linia((cx, y_baix), (x_dre, y_dalt)))
                elif lletra_up == 'W':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_esq + 45, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq + 45, y_baix), (cx, y_mitj)))
                    ruta.extend(self.interpolar_linia((cx, y_mitj), (x_dre - 45, y_baix)))
                    ruta.extend(self.interpolar_linia((x_dre - 45, y_baix), (x_dre, y_dalt)))
                elif lletra_up == 'X':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_dre, y_baix)))
                    ruta.extend(self.interpolar_linia((x_dre, y_dalt), (x_esq, y_baix)))
                elif lletra_up == 'Y':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (cx, y_mitj)))
                    ruta.extend(self.interpolar_linia((x_dre, y_dalt), (cx, y_mitj)))
                    ruta.extend(self.interpolar_linia((cx, y_mitj), (cx, y_baix)))
                elif lletra_up == 'Z':
                    ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_dre, y_dalt)))
                    ruta.extend(self.interpolar_linia((x_dre, y_dalt), (x_esq, y_baix)))
                    ruta.extend(self.interpolar_linia((x_esq, y_baix), (x_dre, y_baix)))

            else: # MINÚSCULES
                y_dalt_min, y_baix_min = cy - 60, cy + 100
                y_mitj_min = cy + 20

                if lletra_lower == 'a':
                    for i in range(30):
                        a = 2 * math.pi * (i / 29.0)
                        ruta.append((int(cx - 15 + 30 * math.cos(a)), int(y_mitj_min + 30 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((cx + 15, y_mitj_min - 20), (cx + 15, y_baix_min)))
                elif lletra_lower == 'b':
                    ruta.extend(self.interpolar_linia((cx - 35, y_dalt_min - 40), (cx - 35, y_baix_min)))
                    for i in range(25):
                        a = 2 * math.pi * (i / 24.0)
                        ruta.append((int(cx + 10 + 30 * math.cos(a)), int(y_mitj_min + 30 * math.sin(a))))
                elif lletra_lower == 'c':
                    for i in range(25):
                        a = math.pi/4 + (1.5 * math.pi) * (i/24.0)
                        ruta.append((int(cx + 25 * math.cos(a)), int(y_mitj_min + 25 * math.sin(a))))
                elif lletra_lower == 'd':
                    for i in range(25):
                        a = 2 * math.pi * (i / 24.0)
                        ruta.append((int(cx - 10 + 30 * math.cos(a)), int(y_mitj_min + 30 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((cx + 20, y_dalt_min - 40), (cx + 20, y_baix_min)))
                elif lletra_lower == 'e':
                    ruta.extend(self.interpolar_linia((cx - 35, y_mitj_min), (cx + 35, y_mitj_min)))
                    for i in range(22):
                        a = math.pi * (i / 21.0)
                        ruta.append((int(cx + 30 * math.cos(a)), int(y_mitj_min - 30 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((cx + 30, y_mitj_min), (cx - 35, y_baix_min)))
                elif lletra_lower == 'f':
                    for i in range(15):
                        a = math.pi/2 + math.pi * (i/14.0)
                        ruta.append((int(cx + 20 + 20 * math.cos(a)), int(y_dalt_min - 20 + 20 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((cx + 20, y_dalt_min), (cx + 20, y_baix_min)))
                    ruta.extend(self.interpolar_linia((cx - 10, y_mitj_min), (cx + 30, y_mitj_min)))
                elif lletra_lower == 'g':
                    for i in range(25):
                        a = 2 * math.pi * (i / 24.0)
                        ruta.append((int(cx - 10 + 30 * math.cos(a)), int(y_mitj_min + 30 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((cx + 20, y_mitj_min), (cx + 20, y_baix_min + 40)))
                    for i in range(12):
                        a = math.pi * (i/11.0)
                        ruta.append((int(cx + 20 - 20 * math.sin(a)), int(y_baix_min + 40 - 20 * (1 - math.cos(a)))))
                elif lletra_lower == 'h':
                    ruta.extend(self.interpolar_linia((cx - 35, y_dalt_min - 40), (cx - 35, y_baix_min)))
                    ruta.extend(self.interpolar_linia((cx - 35, y_mitj_min), (cx + 5, y_mitj_min)))
                    ruta.extend(self.interpolar_linia((cx + 5, y_mitj_min), (cx + 5, y_baix_min)))
                elif lletra_lower == 'i':
                    ruta.extend(self.interpolar_linia((cx, y_mitj_min), (cx, y_baix_min)))
                    ruta.append((cx, y_dalt_min - 10))
                elif lletra_lower == 'j':
                    ruta.extend(self.interpolar_linia((cx, y_mitj_min), (cx, y_baix_min + 30)))
                    for i in range(12):
                        a = math.pi * (i/11.0)
                        ruta.append((int(cx - 20 * math.sin(a)), int(y_baix_min + 30 - 20 * (1 - math.cos(a)))))
                    ruta.append((cx, y_dalt_min - 10))
                elif lletra_lower == 'k':
                    ruta.extend(self.interpolar_linia((cx - 35, y_dalt_min - 40), (cx - 35, y_baix_min)))
                    ruta.extend(self.interpolar_linia((cx + 20, y_mitj_min - 10), (cx - 35, y_mitj_min + 10)))
                    ruta.extend(self.interpolar_linia((cx - 35, y_mitj_min + 10), (cx + 25, y_baix_min)))
                elif lletra_lower == 'l':
                    ruta.extend(self.interpolar_linia((cx, y_dalt_min - 40), (cx, y_baix_min)))
                elif lletra_lower == 'm':
                    ruta.extend(self.interpolar_linia((cx - 40, y_baix_min), (cx - 40, y_mitj_min)))
                    ruta.extend(self.interpolar_linia((cx - 40, y_mitj_min), (cx - 10, y_baix_min)))
                    ruta.extend(self.interpolar_linia((cx - 10, y_baix_min), (cx - 10, y_mitj_min)))
                    ruta.extend(self.interpolar_linia((cx - 10, y_mitj_min), (cx + 25, y_baix_min)))
                elif lletra_lower == 'n':
                    ruta.extend(self.interpolar_linia((cx - 30, y_baix_min), (cx - 30, y_mitj_min)))
                    ruta.extend(self.interpolar_linia((cx - 30, y_mitj_min), (cx + 20, y_baix_min)))
                elif lletra_lower == 'o':
                    for i in range(25):
                        a = 2 * math.pi * (i / 24.0)
                        ruta.append((int(cx + 30 * math.cos(a)), int(y_mitj_min + 30 * math.sin(a))))
                elif lletra_lower == 'p':
                    ruta.extend(self.interpolar_linia((cx - 35, y_mitj_min), (cx - 35, y_baix_min + 40)))
                    for i in range(25):
                        a = 2 * math.pi * (i / 24.0)
                        ruta.append((int(cx + 10 + 30 * math.cos(a)), int(y_mitj_min + 30 * math.sin(a))))
                elif lletra_lower == 'q':
                    for i in range(25):
                        a = 2 * math.pi * (i / 24.0)
                        ruta.append((int(cx - 10 + 30 * math.cos(a)), int(y_mitj_min + 30 * math.sin(a))))
                    ruta.extend(self.interpolar_linia((cx + 20, y_mitj_min), (cx + 20, y_baix_min + 40)))
                elif lletra_lower == 'r':
                    ruta.extend(self.interpolar_linia((cx - 25, y_baix_min), (cx - 25, y_mitj_min)))
                    for i in range(12):
                        a = math.pi * (i/11.0)
                        ruta.append((int(cx - 25 + 20 * math.sin(a)), int(y_mitj_min - 20 * (1 - math.cos(a)))))
                elif lletra_lower == 's':
                    for i in range(18):
                        a = math.pi * (i / 17.0)
                        ruta.append((int(cx + 25 * math.cos(a + math.pi/2)), int(y_mitj_min - 15 + 20 * math.sin(a + math.pi/2))))
                    for i in range(18):
                        a = math.pi * (i / 17.0)
                        ruta.append((int(cx - 25 * math.cos(a + math.pi/2)), int(y_baix_min - 15 + 20 * math.sin(a + math.pi/2))))
                elif lletra_lower == 't':
                    ruta.extend(self.interpolar_linia((cx, y_dalt_min - 20), (cx, y_baix_min)))
                    ruta.extend(self.interpolar_linia((cx - 20, y_mitj_min), (cx + 20, y_mitj_min)))
                elif lletra_lower == 'u':
                    ruta.extend(self.interpolar_linia((cx - 35, y_mitj_min), (cx - 35, y_baix_min - 15)))
                    for i in range(15):
                        a = math.pi * (i / 14.0)
                        ruta.append((int(cx + 35 * math.cos(a - math.pi)), int(y_baix_min - 15 + 15 * math.sin(a - math.pi))))
                    ruta.extend(self.interpolar_linia((cx + 35, y_mitj_min), (cx + 35, y_baix_min)))
                elif lletra_lower == 'v':
                    ruta.extend(self.interpolar_linia((cx - 35, y_mitj_min), (cx, y_baix_min)))
                    ruta.extend(self.interpolar_linia((cx, y_baix_min), (cx + 35, y_mitj_min)))
                elif lletra_lower == 'w':
                    ruta.extend(self.interpolar_linia((cx - 40, y_mitj_min), (cx - 15, y_baix_min)))
                    ruta.extend(self.interpolar_linia((cx - 15, y_baix_min), (cx, y_mitj_min + 15)))
                    ruta.extend(self.interpolar_linia((cx, y_mitj_min + 15), (cx + 15, y_baix_min)))
                    ruta.extend(self.interpolar_linia((cx + 15, y_baix_min), (cx + 40, y_mitj_min)))
                elif lletra_lower == 'x':
                    ruta.extend(self.interpolar_linia((cx - 30, y_mitj_min), (cx + 30, y_baix_min)))
                    ruta.extend(self.interpolar_linia((cx + 30, y_mitj_min), (cx - 30, y_baix_min)))
                elif lletra_lower == 'y':
                    ruta.extend(self.interpolar_linia((cx - 30, y_mitj_min), (cx, y_baix_min + 30)))
                    ruta.extend(self.interpolar_linia((cx + 30, y_mitj_min), (cx - 30, y_baix_min + 40)))
                elif lletra_lower == 'z':
                    ruta.extend(self.interpolar_linia((cx - 30, y_mitj_min), (cx + 30, y_mitj_min)))
                    ruta.extend(self.interpolar_linia((cx + 30, y_mitj_min), (cx - 30, y_baix_min)))
                    ruta.extend(self.interpolar_linia((cx - 30, y_baix_min), (cx + 30, y_baix_min)))

        else: # NOMBRES (0 al 9)
            y_dalt, y_baix = cy - 140, cy + 140
            num = str(element)

            if num == '0':
                for i in range(35):
                    a = 2 * math.pi * (i / 34.0)
                    ruta.append((int(cx + 60 * math.cos(a)), int(cy + 90 * math.sin(a))))
            elif num == '1':
                ruta.extend(self.interpolar_linia((cx - 20, y_dalt + 30), (cx, y_dalt)))
                ruta.extend(self.interpolar_linia((cx, y_dalt), (cx, y_baix)))
                ruta.extend(self.interpolar_linia((cx - 30, y_baix), (cx + 30, y_baix)))
            elif num == '2':
                for i in range(20):
                    a = math.pi/2 + math.pi * (i/19.0)
                    ruta.append((int(cx + 50 * math.cos(a)), int(y_dalt + 50 + 50 * math.sin(a))))
                ruta.extend(self.interpolar_linia((cx + 50, y_dalt + 50), (x_esq, y_baix)))
                ruta.extend(self.interpolar_linia((x_esq, y_baix), (x_dre, y_baix)))
            elif num == '3':
                for i in range(18):
                    a = -math.pi/2 + math.pi * (i/17.0)
                    ruta.append((int(cx + 40 * math.cos(a)), int(cy - 70 + 40 * math.sin(a))))
                for i in range(18):
                    a = -math.pi/2 + math.pi * (i/17.0)
                    ruta.append((int(cx + 40 * math.cos(a)), int(cy + 70 + 40 * math.sin(a))))
            elif num == '4':
                ruta.extend(self.interpolar_linia((x_dre - 20, y_dalt), (x_esq + 20, cy + 30)))
                ruta.extend(self.interpolar_linia((x_esq + 20, cy + 30), (x_dre, cy + 30)))
                ruta.extend(self.interpolar_linia((cx + 20, y_dalt), (cx + 20, y_baix)))
            elif num == '5':
                ruta.extend(self.interpolar_linia((x_dre, y_dalt), (x_esq, y_dalt)))
                ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_esq, cy)))
                for i in range(20):
                    a = -math.pi/2 + 1.5 * math.pi * (i/19.0)
                    ruta.append((int(cx + 50 * math.cos(a)), int(cy + 50 + 50 * math.sin(a))))
            elif num == '6':
                for i in range(20):
                    a = math.pi/2 + math.pi * (i/19.0)
                    ruta.append((int(cx + 20 + 50 * math.cos(a)), int(y_dalt + 50 + 50 * math.sin(a))))
                for i in range(25):
                    a = 2 * math.pi * (i / 24.0)
                    ruta.append((int(cx + 10 + 45 * math.cos(a)), int(cy + 45 + 45 * math.sin(a))))
            elif num == '7':
                ruta.extend(self.interpolar_linia((x_esq, y_dalt), (x_dre, y_dalt)))
                ruta.extend(self.interpolar_linia((x_dre, y_dalt), (x_esq + 20, y_baix)))
            elif num == '8':
                for i in range(20):
                    a = 2 * math.pi * (i / 19.0)
                    ruta.append((int(cx + 40 * math.cos(a)), int(cy - 60 + 40 * math.sin(a))))
                for i in range(20):
                    a = 2 * math.pi * (i / 19.0)
                    ruta.append((int(cx + 50 * math.cos(a)), int(cy + 60 + 50 * math.sin(a))))
            elif num == '9':
                for i in range(25):
                    a = 2 * math.pi * (i / 24.0)
                    ruta.append((int(cx + 10 + 45 * math.cos(a)), int(cy - 45 + 45 * math.sin(a))))
                ruta.extend(self.interpolar_linia((cx + 55, cy - 45), (cx - 30, y_baix)))

        # FALLBACK VECTORIAL NET I FLUID (si no coincideix exactament)
        if not ruta:
            p_inici = (cx - 50, cy - 80)
            p_mig = (cx, cy)
            p_final = (cx + 50, cy + 80)
            ruta.extend(self.interpolar_linia(p_inici, p_mig, 30))
            ruta.extend(self.interpolar_linia(p_mig, p_final, 30))

        return ruta

    def dibuixar_letra_estatica(self, element, pos=(640, 360)):
        txt = self.font_gran.render(str(element), True, self.GRIS_Guia)
        rect = txt.get_rect(center=pos)
        self.pantalla.blit(txt, rect)
        return rect

    def dibuixar_animacio_traç(self, element, ruta_punts, progres, limit_progres=120):
        self.dibuixar_letra_estatica(element)
        
        if not ruta_punts:
            return

        total_punts = len(ruta_punts)
        index_actual = int((progres / limit_progres) * total_punts)
        index_actual = min(index_actual, total_punts - 1)
        
        if index_actual > 0:
            sub_ruta = ruta_punts[:index_actual + 1]
            pygame.draw.aalines(self.pantalla, self.VERMELL_Traç, False, sub_ruta, 18)
            for p in sub_ruta:
                pygame.draw.circle(self.pantalla, self.VERMELL_Traç, p, 9)

        punter_actual = ruta_punts[index_actual]
        halo_surf = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(halo_surf, (231, 76, 60, 90), (30, 30), 26)
        pygame.draw.circle(halo_surf, (255, 255, 255, 160), (30, 30), 14)
        
        self.pantalla.blit(halo_surf, (punter_actual[0] - 30, punter_actual[1] - 30))

        txt_fase = self.font_petita.render("Fase 1: Mira atentament com s'escriu", True, self.TEXT_Color)
        self.pantalla.blit(txt_fase, (50, self.alcada - 60))

    def dibuixar_resseguit(self, element, punts_nen, pos=(640, 360)):
        self.dibuixar_letra_estatica(element, pos)
        if len(punts_nen) > 1:
            pygame.draw.aalines(self.pantalla, self.VERMELL_Traç, False, punts_nen, 18)
            for p in punts_nen:
                pygame.draw.circle(self.pantalla, self.VERMELL_Traç, p, 12)

        txt_fase = self.font_petita.render("Fase 2: Ressegueix amb el dit a la pissarra!", True, self.TEXT_Color)
        self.pantalla.blit(txt_fase, (50, self.alcada - 60))

    def dibuixar_traç_final(self, punts_nen):
        if len(punts_nen) > 1:
            pygame.draw.aalines(self.pantalla, self.VERMELL_Traç, False, punts_nen, 18)
            for p in punts_nen:
                pygame.draw.circle(self.pantalla, self.VERMELL_Traç, p, 12)

    def crear_confeti(self):
        self.confeti = []
        colors = [(231, 76, 60), (46, 204, 113), (52, 152, 219), (241, 196, 15), (155, 89, 182)]
        for _ in range(150):
            self.confeti.append({
                'x': random.randint(0, self.amplada),
                'y': random.randint(-self.alcada, 0),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(3, 7),
                'color': random.choice(colors),
                'radi': random.randint(5, 10)
            })

    def actualitzar_i_dibuixar_confeti(self):
        for c in self.confeti:
            c['x'] += c['vx']
            c['y'] += c['vy']
            if c['y'] > self.alcada:
                c['y'] = random.randint(-50, 0)
                c['x'] = random.randint(0, self.amplada)
            pygame.draw.circle(self.pantalla, c['color'], (int(c['x']), int(c['y'])), c['radi'])

    def dibuixar_botons_finals(self):
        boto_repetir_rect = pygame.Rect(self.amplada // 2 - 450, 130, 280, 65)
        boto_canviar_rect = pygame.Rect(self.amplada // 2 - 140, 130, 280, 65)
        boto_mode_rect = pygame.Rect(self.amplada // 2 + 170, 130, 280, 65)

        pygame.draw.rect(self.pantalla, self.BLAU_Botó, boto_repetir_rect, border_radius=16)
        pygame.draw.rect(self.pantalla, self.VERD_Exit, boto_canviar_rect, border_radius=16)
        pygame.draw.rect(self.pantalla, self.Taronja_Opcio, boto_mode_rect, border_radius=16)

        txt_rep = self.font_mitjana.render("Tornar a repetir", True, self.BLANC)
        txt_can = self.font_mitjana.render("Canviar", True, self.BLANC)
        txt_mode = self.font_mitjana.render("Menú principal", True, self.BLANC)

        self.pantalla.blit(txt_rep, txt_rep.get_rect(center=boto_repetir_rect.center))
        self.pantalla.blit(txt_can, txt_can.get_rect(center=boto_canviar_rect.center))
        self.pantalla.blit(txt_mode, txt_mode.get_rect(center=boto_mode_rect.center))

        return boto_repetir_rect, boto_canviar_rect, boto_mode_rect

    def actualitzar_pantalla(self):
        pygame.display.flip()
        self.rellotge.tick(60)