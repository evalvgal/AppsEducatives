"""
Controlador principal (MVC) de l'aplicació de Suma de Fraccions.
Coordina la navegació entre el menú principal de 2 parts (mateix denominador
i diferents denominadors), l'avançament de passos, la generació de nous
exercicis i el tancament amb la tecla ESC.
"""
import sys
import pygame

from diccionariSumaFraccio import generar_exercici_fraccio
from grafics_sumaFraccio import VistaSumaFraccio


class ControladorSumaFraccio:
    def __init__(self):
        self.vista = VistaSumaFraccio()
        self.estat = "MENU"  # MENU o EXERCICI
        self.mateix_denominador = True
        self.exercici_actual = None
        self.pas_actual = 0
        self.rects_actius = {}

    def iniciar_modalitat(self, mateix_denominador):
        self.mateix_denominador = mateix_denominador
        self.exercici_actual = generar_exercici_fraccio(mateix_denominador)
        self.pas_actual = 0
        self.estat = "EXERCICI"

    def nou_exercici(self):
        ultim = self.exercici_actual.get("clau") if self.exercici_actual else None
        self.exercici_actual = generar_exercici_fraccio(self.mateix_denominador, ultim_exercici=ultim)
        self.pas_actual = 0

    def avancar_pas(self):
        if not self.exercici_actual:
            return
        total = len(self.exercici_actual["passos"])
        if self.pas_actual < total:
            self.pas_actual += 1

    def sortir(self):
        pygame.quit()
        sys.exit()

    def gestionar_esdeveniments(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.sortir()

            elif event.type == pygame.VIDEORESIZE:
                self.vista.gestionar_redimensio(event.w, event.h)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.sortir()
                elif event.key == pygame.K_F11:
                    self.vista.alternar_pantalla_completa()
                elif self.estat == "EXERCICI":
                    if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.avancar_pas()
                    elif event.key == pygame.K_n:
                        self.nou_exercici()

            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button != 1:
                    continue

                pos = (
                    event.pos
                    if event.type == pygame.MOUSEBUTTONDOWN
                    else (int(event.x * self.vista.amplada), int(event.y * self.vista.alcada))
                )

                if self.vista.obtenir_rect_sortir().collidepoint(pos):
                    self.sortir()

                if self.estat == "MENU":
                    if "mateix_den" in self.rects_actius and self.rects_actius["mateix_den"].collidepoint(pos):
                        self.iniciar_modalitat(True)
                    elif "diferent_den" in self.rects_actius and self.rects_actius["diferent_den"].collidepoint(pos):
                        self.iniciar_modalitat(False)

                elif self.estat == "EXERCICI":
                    if "enrere" in self.rects_actius and self.rects_actius["enrere"].collidepoint(pos):
                        self.estat = "MENU"
                    elif "seguent_pas" in self.rects_actius and self.rects_actius["seguent_pas"].collidepoint(pos):
                        self.avancar_pas()
                    elif "nou_exercici" in self.rects_actius and self.rects_actius["nou_exercici"].collidepoint(pos):
                        self.nou_exercici()

    def renderitzar(self):
        if self.estat == "MENU":
            self.rects_actius = self.vista.dibuixar_menu_principal()
        elif self.estat == "EXERCICI":
            self.rects_actius = self.vista.dibuixar_exercici(self.exercici_actual, self.pas_actual)

    def executar(self):
        while True:
            self.gestionar_esdeveniments()
            self.renderitzar()
            self.vista.actualitzar()


if __name__ == "__main__":
    app = ControladorSumaFraccio()
    app.executar()