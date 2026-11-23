"""
Controlador principal (MVC) de l'aplicació de Multiplicació de Fraccions.
Coordina l'avançament de passos, la generació de nous exercicis amb fraccions
aleatòries de l'1 al 30 i el tancament amb la tecla ESC.
"""
import sys
import pygame

from diccionariMultiplicaFraccio import generar_exercici_multiplicacio
from grafics_multiplicaFraccio import VistaMultiplicaFraccio


class ControladorMultiplicaFraccio:
    def __init__(self):
        self.vista = VistaMultiplicaFraccio()
        self.exercici_actual = generar_exercici_multiplicacio()
        self.pas_actual = 0
        self.rects_actius = {}

    def nou_exercici(self):
        ultim = self.exercici_actual.get("clau") if self.exercici_actual else None
        self.exercici_actual = generar_exercici_multiplicacio(ultim_exercici=ultim)
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
                elif event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER):
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

                if "seguent_pas" in self.rects_actius and self.rects_actius["seguent_pas"].collidepoint(pos):
                    self.avancar_pas()
                elif "nou_exercici" in self.rects_actius and self.rects_actius["nou_exercici"].collidepoint(pos):
                    self.nou_exercici()

    def renderitzar(self):
        self.rects_actius = self.vista.dibuixar_exercici(self.exercici_actual, self.pas_actual)

    def executar(self):
        while True:
            self.gestionar_esdeveniments()
            self.renderitzar()
            self.vista.actualitzar()


if __name__ == "__main__":
    app = ControladorMultiplicaFraccio()
    app.executar()