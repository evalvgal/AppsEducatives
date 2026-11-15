import sys
import pygame
import random
from grafics_diftongshiat import VistaDiftongsHiat
from diccionaridiftongshiat import DADES_TEORIA, BANCH_EXERCICIS

class JocDiftongsHiat:
    def __init__(self):
        self.vista = VistaDiftongsHiat()
        self.estat = "MENU_PRINCIPAL"
        
        self.exercici_actual = None
        self.resposta_tipus_seleccionada = None
        self.text_silabes_usuari = ""
        self.feedback = None
        self.carregar_nou_exercici()

    def carregar_nou_exercici(self):
        self.exercici_actual = random.choice(BANCH_EXERCICIS)
        self.resposta_tipus_seleccionada = None
        self.text_silabes_usuari = ""
        self.feedback = None

    def executar(self):
        while True:
            self.gestionar_esdeveniments()
            self.renderitzar()
            self.vista.actualitzar_pantalla()

    def gestionar_esdeveniments(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.tancar_aplicacio()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.tancar_aplicacio()
                elif event.key == pygame.K_F11:
                    pygame.display.toggle_fullscreen()

                elif self.estat == "PANTALLA_EXERCICI":
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if self.feedback is not None:
                            self.carregar_nou_exercici()
                        else:
                            self.validar_exercici()
                    elif self.feedback is None:
                        if event.key == pygame.K_BACKSPACE:
                            self.text_silabes_usuari = self.text_silabes_usuari[:-1]
                        else:
                            if event.unicode.isprintable() and len(event.unicode) > 0:
                                self.text_silabes_usuari += event.unicode

            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                pos = event.pos if event.type == pygame.MOUSEBUTTONDOWN else (int(event.x * self.vista.amplada), int(event.y * self.vista.alcada))

                if self.vista.obtenir_rect_sortir().collidepoint(pos):
                    self.tancar_aplicacio()

                if self.estat == "MENU_PRINCIPAL":
                    b_dif, b_hia, b_exe = self.vista.dibuixar_menu_principal()
                    if b_dif.collidepoint(pos):
                        self.estat = "PANTALLA_DIFTONGS"
                    elif b_hia.collidepoint(pos):
                        self.estat = "PANTALLA_HIATS"
                    elif b_exe.collidepoint(pos):
                        self.estat = "PANTALLA_EXERCICI"
                        self.carregar_nou_exercici()

                elif self.estat in ("PANTALLA_DIFTONGS", "PANTALLA_HIATS", "PANTALLA_EXERCICI"):
                    b_enrere = self.vista.dibuixar_boto_enrere()
                    if b_enrere.collidepoint(pos):
                        self.estat = "MENU_PRINCIPAL"

                    if self.estat == "PANTALLA_EXERCICI":
                        ample_caixa = 1040
                        caixa = pygame.Rect(self.vista.amplada // 2 - ample_caixa // 2, 105, ample_caixa, self.vista.alcada - 195)
                        w_btn, h_btn = 290, 52
                        espaiat = 25
                        ample_total_btns = (3 * w_btn) + (2 * espaiat)
                        inici_x_btns = caixa.centerx - ample_total_btns // 2
                        y_btns = caixa.y + 140

                        b_creixent = pygame.Rect(inici_x_btns, y_btns, w_btn, h_btn)
                        b_decreixent = pygame.Rect(inici_x_btns + w_btn + espaiat, y_btns, w_btn, h_btn)
                        b_hiat = pygame.Rect(inici_x_btns + (w_btn + espaiat) * 2, y_btns, w_btn, h_btn)
                        b_validar = pygame.Rect(caixa.centerx - 190, caixa.y + caixa.height - 70, 380, 52)

                        if b_creixent.collidepoint(pos) and self.feedback is None:
                            self.resposta_tipus_seleccionada = "creixent"
                        elif b_decreixent.collidepoint(pos) and self.feedback is None:
                            self.resposta_tipus_seleccionada = "decreixent"
                        elif b_hiat.collidepoint(pos) and self.feedback is None:
                            self.resposta_tipus_seleccionada = "hiat"
                        elif b_validar.collidepoint(pos):
                            if self.feedback is not None:
                                self.carregar_nou_exercici()
                            else:
                                self.validar_exercici()

    def validar_exercici(self):
        noms_complets = {
            "creixent": "Diftong Creixent",
            "decreixent": "Diftong Decreixent",
            "hiat": "Hiat"
        }

        tipus_correcte = self.exercici_actual["tipus"]
        silabes_correctes_orig = self.exercici_actual["silabes_correctes"]

        # Validació 1: Fenomen (Creixent, Decreixent o Hiat)
        fenomen_ok = (self.resposta_tipus_seleccionada == tipus_correcte)
        if fenomen_ok:
            msg_fenomen = f"Correcte! És un {noms_complets[tipus_correcte]}."
        else:
            msg_fenomen = f"Incorrecte. La resposta correcta és: {noms_complets[tipus_correcte]}."

        # Validació 2: Síl·labes (ignorem espais al voltant dels guions per ser flexibles)
        sil_usuari_norm = self.text_silabes_usuari.replace(" ", "").lower()
        sil_correcta_norm = silabes_correctes_orig.replace(" ", "").lower()

        silabes_ok = (sil_usuari_norm == sil_correcta_norm)
        if silabes_ok:
            msg_silabes = f"Correcte! Separació: {silabes_correctes_orig}"
        else:
            msg_silabes = f"Incorrecte. Separació correcta: {silabes_correctes_orig}"

        self.feedback = {
            "fenomen_ok": fenomen_ok,
            "msg_fenomen": msg_fenomen,
            "silabes_ok": silabes_ok,
            "msg_silabes": msg_silabes
        }

    def renderitzar(self):
        if self.estat == "MENU_PRINCIPAL":
            self.vista.dibuixar_menu_principal()
        elif self.estat == "PANTALLA_DIFTONGS":
            self.vista.dibuixar_pantalla_diftongs(DADES_TEORIA["diftongs"])
        elif self.estat == "PANTALLA_HIATS":
            self.vista.dibuixar_pantalla_hiats(DADES_TEORIA["hiats"])
        elif self.estat == "PANTALLA_EXERCICI":
            self.vista.dibuixar_pantalla_exercici(
                self.exercici_actual, 
                self.feedback, 
                self.resposta_tipus_seleccionada, 
                self.text_silabes_usuari
            )

    def tancar_aplicacio(self):
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    joc = JocDiftongsHiat()
    joc.executar()