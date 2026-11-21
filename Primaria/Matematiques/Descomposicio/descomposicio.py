# -*- coding: utf-8 -*-
import sys
import pygame

from diccionariDescomposicio import (
    TEORIA_PAGINA_1,
    TEORIA_PAGINA_2,
    generar_exercici_aleatori,
)
from grafics_descomposicio import VistaDescomposicio


class ControladorDescomposicio:
    def __init__(self):
        self.vista = VistaDescomposicio()
        self.estat = "MENU"  # MENU, TEORIA_1, TEORIA_2, EXERCICIS
        self.exercici_actual = generar_exercici_aleatori()
        self.passos_mostrats = 0
        self.rects_actius = {}

    def nou_exercici(self):
        ultim = self.exercici_actual["nombre"] if self.exercici_actual else None
        self.exercici_actual = generar_exercici_aleatori(ultim_nombre=ultim)
        self.passos_mostrats = 0

    def avancar_pas(self):
        total = len(self.exercici_actual["passos"])
        if self.passos_mostrats < total:
            self.passos_mostrats += 1

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
            self.rects_actius = self.vista.dibuixar_exercicis(self.exercici_actual, self.passos_mostrats)

    def executar(self):
        while True:
            self.gestionar_esdeveniments()
            self.renderitzar()
            self.vista.actualitzar()


if __name__ == "__main__":
    app = ControladorDescomposicio()
    app.executar()