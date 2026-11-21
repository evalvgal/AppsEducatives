"""
Controlador principal (MVC) de l'aplicació de Mínim Comú Múltiple (m.c.m.)
i Màxim Comú Divisor (M.C.D.).
Coordina la navegació entre el menú principal, les dues pàgines de teoria
i els exercicis resolts pas a pas, així com els esdeveniments de ratolí,
tàctils i de teclat (ESC per sortir i F11 per alternar pantalla completa).
"""
import sys
import pygame

from diccionarimcmMcd import (
    TEORIA_PAGINA_1,
    TEORIA_PAGINA_2,
    generar_exercici_aleatori,
)
from grafics_mcmMcd import VistaMcmMcd


class ControladorMcmMcd:
    def __init__(self):
        self.vista = VistaMcmMcd()
        self.estat = "MENU"  # MENU, TEORIA_1, TEORIA_2, EXERCICIS
        self.exercici_actual = generar_exercici_aleatori()
        self.etapa_actual = 0
        self.rects_actius = {}

    def _total_etapes_exercici(self):
        nx = len(self.exercici_actual["passos_x"])
        ny = len(self.exercici_actual["passos_y"])
        return nx + ny + 2

    def nou_exercici(self):
        ultima = (self.exercici_actual["x"], self.exercici_actual["y"]) if self.exercici_actual else None
        self.exercici_actual = generar_exercici_aleatori(ultima_parella=ultima)
        self.etapa_actual = 0

    def avancar_pas(self):
        total = self._total_etapes_exercici()
        if self.etapa_actual < total:
            self.etapa_actual += 1

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
                elif self.estat == "EXERCICIS":
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
                    if "teoria" in self.rects_actius and self.rects_actius["teoria"].collidepoint(pos):
                        self.estat = "TEORIA_1"
                    elif "exercicis" in self.rects_actius and self.rects_actius["exercicis"].collidepoint(pos):
                        self.estat = "EXERCICIS"
                        self.nou_exercici()

                elif self.estat == "TEORIA_1":
                    if "enrere" in self.rects_actius and self.rects_actius["enrere"].collidepoint(pos):
                        self.estat = "MENU"
                    elif "pagina_2" in self.rects_actius and self.rects_actius["pagina_2"].collidepoint(pos):
                        self.estat = "TEORIA_2"

                elif self.estat == "TEORIA_2":
                    if "enrere" in self.rects_actius and self.rects_actius["enrere"].collidepoint(pos):
                        self.estat = "MENU"
                    elif "pagina_1" in self.rects_actius and self.rects_actius["pagina_1"].collidepoint(pos):
                        self.estat = "TEORIA_1"

                elif self.estat == "EXERCICIS":
                    if "enrere" in self.rects_actius and self.rects_actius["enrere"].collidepoint(pos):
                        self.estat = "MENU"
                    elif "seguent_pas" in self.rects_actius and self.rects_actius["seguent_pas"].collidepoint(pos):
                        self.avancar_pas()
                    elif "nou_exercici" in self.rects_actius and self.rects_actius["nou_exercici"].collidepoint(pos):
                        self.nou_exercici()

    def renderitzar(self):
        if self.estat == "MENU":
            self.rects_actius = self.vista.dibuixar_menu_principal()
        elif self.estat == "TEORIA_1":
            self.rects_actius = self.vista.dibuixar_teoria_pagina_1(TEORIA_PAGINA_1)
        elif self.estat == "TEORIA_2":
            self.rects_actius = self.vista.dibuixar_teoria_pagina_2(TEORIA_PAGINA_2)
        elif self.estat == "EXERCICIS":
            self.rects_actius = self.vista.dibuixar_exercicis(self.exercici_actual, self.etapa_actual)

    def executar(self):
        while True:
            self.gestionar_esdeveniments()
            self.renderitzar()
            self.vista.actualitzar()


if __name__ == "__main__":
    app = ControladorMcmMcd()
    app.executar()