import sys
import math
import pygame
from grafics_nombreslletres import VistaLectoEscriptura

class JocLectoEscriptura:
    def __init__(self):
        self.vista = VistaLectoEscriptura()
        # Estats: MENU_PRINCIPAL, MENU_INICIAL (Maj/Min), ESPECIFICAR_ELEMENT, FASE_ANIMACIO, FASE_RESSEGUIR, CELEBRACIO
        self.estat = "MENU_PRINCIPAL"  
        self.practica = "LLETRA" # "LLETRA" o "NOMBRE"
        self.tipus_lletra = "MAJUSCULA" # "MAJUSCULA" o "MINUSCULA"
        self.element_actual = ""
        self.progres_animacio = 0
        self.ruta_animacio = []
        self.longitud_esperada = 500
        
        self.traços_nen = [] 
        self.traç_actual = []
        self.pressionat = False

    def executar(self):
        while True:
            self.gestionar_esdeveniments()
            self.actualitzar_logica()
            self.renderitzar()

    def gestionar_esdeveniments(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.tancar_programa()

            # Sortir immediatament prement la tecla ESC en qualsevol moment
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.tancar_programa()

            # 1. Clics de ratolí o tàctils
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                pos = event.pos if event.type == pygame.MOUSEBUTTONDOWN else (int(event.x * self.vista.amplada), int(event.y * self.vista.alcada))
                
                # Botó de SORTIR global
                if self.vista.obtenir_rect_sortir().collidepoint(pos):
                    self.tancar_programa()

                if self.estat == "MENU_PRINCIPAL":
                    boto_nombres, boto_lletres = self.vista.dibuixar_menu_principal()
                    if boto_nombres.collidepoint(pos):
                        self.practica = "NOMBRE"
                        self.estat = "ESPECIFICAR_ELEMENT"
                        self.element_actual = ""
                    elif boto_lletres.collidepoint(pos):
                        self.practica = "LLETRA"
                        self.estat = "MENU_INICIAL" # Va al menú de triar majúscules o minúscules
                        self.element_actual = ""

                elif self.estat == "MENU_INICIAL":
                    boto_maj, boto_min = self.vista.dibuixar_menu_inicial()
                    if boto_maj.collidepoint(pos):
                        self.tipus_lletra = "MAJUSCULA"
                        self.estat = "ESPECIFICAR_ELEMENT"
                        self.element_actual = ""
                    elif boto_min.collidepoint(pos):
                        self.tipus_lletra = "MINUSCULA"
                        self.estat = "ESPECIFICAR_ELEMENT"
                        self.element_actual = ""

                elif self.estat == "FASE_RESSEGUIR":
                    self.pressionat = True
                    self.traç_actual = [pos]

                elif self.estat == "CELEBRACIO":
                    boto_rep, boto_can, boto_mode = self.vista.dibuixar_botons_finals()
                    if boto_rep.collidepoint(pos):
                        # Repetir el mateix element
                        self.traços_nen = []
                        self.traç_actual = []
                        self.ruta_animacio = self.vista.generar_ruta_element(self.element_actual, self.practica, self.tipus_lletra)
                        self.longitud_esperada = self.calcular_longitud_ruta(self.ruta_animacio)
                        self.estat = "FASE_ANIMACIO"
                        self.progres_animacio = 0
                    elif boto_can.collidepoint(pos):
                        # Canviar només d'element
                        self.estat = "ESPECIFICAR_ELEMENT"
                        self.element_actual = ""
                        self.traços_nen = []
                        self.traç_actual = []
                    elif boto_mode.collidepoint(pos):
                        # Tornar al menú principal (Nombres / Lletres)
                        self.estat = "MENU_PRINCIPAL"
                        self.element_actual = ""
                        self.traços_nen = []
                        self.traç_actual = []

            # 2. Entrada de tecles per part del professor
            elif event.type == pygame.KEYDOWN and self.estat == "ESPECIFICAR_ELEMENT":
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if self.element_actual.strip():
                        self.ruta_animacio = self.vista.generar_ruta_element(self.element_actual, self.practica, self.tipus_lletra)
                        self.longitud_esperada = self.calcular_longitud_ruta(self.ruta_animacio)
                        self.estat = "FASE_ANIMACIO"
                        self.progres_animacio = 0
                elif event.key == pygame.K_BACKSPACE:
                    self.element_actual = ""
                else:
                    caracter = event.unicode
                    if self.practica == "LLETRA":
                        if caracter.isalpha():
                            if self.tipus_lletra == "MAJUSCULA":
                                self.element_actual = caracter.upper()
                            else:
                                self.element_actual = caracter.lower()
                    else: # NOMBRE
                        if caracter.isdigit():
                            self.element_actual = caracter

            # 3. Gestió del traç tàctil a la Fase 2
            elif self.estat == "FASE_RESSEGUIR":
                if event.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION) and self.pressionat:
                    pos = event.pos if event.type == pygame.MOUSEMOTION else (int(event.x * self.vista.amplada), int(event.y * self.vista.alcada))
                    self.traç_actual.append(pos)

                elif event.type in (pygame.MOUSEBUTTONUP, pygame.FINGERUP):
                    if self.pressionat and len(self.traç_actual) > 1:
                        self.traços_nen.append(self.traç_actual)
                    self.pressionat = False
                    self.traç_actual = []

                    longitud_total = self.calcular_longitud_total_traços()
                    
                    # Llindar adaptatiu segons el tipus de pràctica
                    if self.practica == "NOMBRE":
                        validat = longitud_total > (self.longitud_esperada * 0.55)
                    elif self.tipus_lletra == "MINUSCULA":
                        validat = longitud_total > (self.longitud_esperada * 0.55)
                    else:
                        validat = longitud_total > (self.longitud_esperada * 0.70)
                    
                    if validat:
                        self.estat = "CELEBRACIO"
                        self.vista.crear_confeti()

    def calcular_longitud_total_traços(self):
        longitud = 0
        for traç in self.traços_nen:
            for i in range(1, len(traç)):
                p1 = traç[i-1]
                p2 = traç[i]
                longitud += math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        return longitud

    def calcular_longitud_ruta(self, ruta):
        if len(ruta) < 2:
            return 500
        longitud = 0
        for i in range(1, len(ruta)):
            p1 = ruta[i-1]
            p2 = ruta[i]
            longitud += math.hypot(p2[0] - p1[0], p2[1] - p1[1])
        return longitud

    def tancar_programa(self):
        pygame.quit()
        sys.exit()

    def actualitzar_logica(self):
        if self.estat == "FASE_ANIMACIO":
            self.progres_animacio += 1
            if self.progres_animacio > 240:
                self.estat = "FASE_RESSEGUIR"

    def renderitzar(self):
        missatge = obtenir_missatge_estat(self.estat, self.element_actual, self.practica)
        self.vista.dibuixar_fons(missatge)

        # Dibuixar botó de sortir
        self.vista.dibuixar_boto_sortir()

        if self.estat == "MENU_PRINCIPAL":
            self.vista.dibuixar_menu_principal()
        elif self.estat == "MENU_INICIAL":
            self.vista.dibuixar_menu_inicial()
        elif self.estat == "ESPECIFICAR_ELEMENT":
            self.vista.dibuixar_pantalla_entrada_element(self.element_actual, self.practica, self.tipus_lletra)
        elif self.estat == "FASE_ANIMACIO":
            self.vista.dibuixar_animacio_traç(self.element_actual, self.ruta_animacio, self.progres_animacio, limit_progres=240)
        elif self.estat == "FASE_RESSEGUIR":
            self.vista.dibuixar_letra_estatica(self.element_actual)
            for traç in self.traços_nen:
                self.vista.dibuixar_traç_final(traç)
            if self.pressionat and len(self.traç_actual) > 1:
                self.vista.dibuixar_traç_final(self.traç_actual)
        elif self.estat == "CELEBRACIO":
            self.vista.dibuixar_letra_estatica(self.element_actual)
            for traç in self.traços_nen:
                self.vista.dibuixar_traç_final(traç)
            self.vista.actualitzar_i_dibuixar_confeti()
            self.vista.dibuixar_botons_finals()

        self.vista.actualitzar_pantalla()

def obtenir_missatge_estat(estat, element, practica):
    if estat == "MENU_PRINCIPAL":
        return "Professorat: Què vols practicar?"
    elif estat == "MENU_INICIAL":
        return "Professorat: Selecciona el tipus de lletra"
    elif estat == "ESPECIFICAR_ELEMENT":
        return "Professorat: Escriu un caràcter al teclat"
    elif estat == "FASE_ANIMACIO":
        tipo = "el nombre" if practica == "NOMBRE" else "la lletra"
        return f"Torn de la classe: Escrivim {tipo} '{element}'"
    elif estat == "FASE_RESSEGUIR":
        return f"Vine a la pissarra i ressegueix el '{element}'!"
    elif estat == "CELEBRACIO":
        return "Molt bé! Campió/a!"
    return ""

if __name__ == "__main__":
    joc = JocLectoEscriptura()
    joc.executar()