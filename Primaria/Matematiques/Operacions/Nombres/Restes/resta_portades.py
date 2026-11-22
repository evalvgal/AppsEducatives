"""
Resta amb Portades — Model lògic, dades i càlculs de restes.
"""

import random
from enum import Enum, auto

class Phase(Enum):
    STEP_UNITS    = auto()   # Avaluant les unitats
    PRE_BORROW_U  = auto()   # Mostrant l'1 lila estàtic a sobre de les unitats
    ANIM_BORROW_U = auto()   # Animant la portada de les Unitats cap a sota de les Decenes
    ADD_CARRY_T   = auto()   # Sumar la portada al subtrahend a sota i netejar l'1 de sobre
    STEP_TENS     = auto()   # Avaluant les decenes
    PRE_BORROW_T  = auto()   # Mostrant l'1 lila estàtic a sobre de les decenes
    ANIM_BORROW_T = auto()   # Animant la portada de les Decenes cap a sota de les Centenes
    ADD_CARRY_H   = auto()   # Sumar la portada al subtrahend a sota i netejar l'1 de sobre
    STEP_HUNDS    = auto()   # Avaluant les centenes
    DONE          = auto()   # Operació acabada

class RestaModel:
    def __init__(self) -> None:
        self.new_problem()

    def new_problem(self) -> None:
        while True:
            a = random.randint(100, 999)
            b = random.randint(10, a - 1)
            au, bu = a % 10, b % 10
            ad, bd = (a // 10) % 10, (b // 10) % 10
            if au < bu or ad < bd:
                break

        self.num_a = a
        self.num_b = b
        self.num_result = a - b

        self.digits_a = [a // 100, (a // 10) % 10, a % 10]
        self.digits_b = [b // 100, (b // 10) % 10, b % 10]

        self.phase: Phase = Phase.STEP_UNITS
        self.borrow_u_active: bool = False  
        self.borrow_d_active: bool = False  
        
        self.carry_u_resolved: bool = False
        self.carry_d_resolved: bool = False

        self.top_u_shown: bool = False
        self.top_d_shown: bool = False

        self.result_u_shown: bool = False
        self.result_d_shown: bool = False
        self.result_h_shown: bool = False

        self.message: str = "Comencem restant les UNITATS!"
        self.message_color: tuple[int, int, int] = (50, 40, 80)
        self.is_finished: bool = False
        self.need_anim_u: bool = False
        self.need_anim_t: bool = False

    def advance_step(self) -> None:
        self.need_anim_u = False
        self.need_anim_t = False

        match self.phase:

            case Phase.STEP_UNITS:
                if self.digits_a[2] < self.digits_b[2]:
                    self.phase = Phase.PRE_BORROW_U
                    self.top_u_shown = True
                    val_top = self.digits_a[2] + 10
                    self.message = f"Com que {self.digits_a[2]} és menor que {self.digits_b[2]}, hi posem un 1 a sobre per convertir-lo en {val_top}."
                else:
                    self.result_u_shown = True
                    self.phase = Phase.STEP_TENS
                    res = self.digits_a[2] - self.digits_b[2]
                    self.message = f"{self.digits_a[2]} − {self.digits_b[2]} = {res}. Passem a les DECENES!"

            case Phase.PRE_BORROW_U:
                self.result_u_shown = True
                self.phase = Phase.ANIM_BORROW_U
                val_top = self.digits_a[2] + 10
                res = val_top - self.digits_b[2]
                self.message = f"De {self.digits_b[2]} a {val_top} hi van {res}! I enviem 1 de portada a sota."
                self.need_anim_u = True

            case Phase.ANIM_BORROW_U:
                pass 

            case Phase.ADD_CARRY_T:
                self.carry_u_resolved = True
                self.top_u_shown = False 
                self.phase = Phase.STEP_TENS
                val_b_actual = self.digits_b[1] + 1
                self.message = f"Fantàstic! El número inferior es converteix en un {val_b_actual}. Anem a mirar les decenes."

            case Phase.STEP_TENS:
                val_bottom = self.digits_b[1] + (1 if self.borrow_u_active else 0)
                
                if self.digits_a[1] < val_bottom:
                    self.phase = Phase.PRE_BORROW_T
                    self.top_d_shown = True
                    val_top = self.digits_a[1] + 10
                    self.message = f"Com que {self.digits_a[1]} és menor que {val_bottom}, hi posem un 1 a sobre per convertir-lo en {val_top}."
                else:
                    self.result_d_shown = True
                    self.phase = Phase.STEP_HUNDS
                    res = self.digits_a[1] - val_bottom
                    self.message = f"{self.digits_a[1]} − {val_bottom} = {res}. Ara a les CENTENES!"

            case Phase.PRE_BORROW_T:
                self.result_d_shown = True
                self.phase = Phase.ANIM_BORROW_T
                val_bottom = self.digits_b[1] + (1 if self.borrow_u_active else 0)
                val_top = self.digits_a[1] + 10
                res = val_top - val_bottom
                self.message = f"De {val_bottom} a {val_top} hi van {res}! Enviem 1 de portada a sota al següent."
                self.need_anim_t = True

            case Phase.ANIM_BORROW_T:
                pass

            case Phase.ADD_CARRY_H:
                self.carry_d_resolved = True
                self.top_d_shown = False
                self.phase = Phase.STEP_HUNDS
                val_b_actual = self.digits_b[0] + 1
                self.message = f"Això és! El número inferior es converteix en un {val_b_actual}. Anem pel darrer pas."

            case Phase.STEP_HUNDS:
                self.result_h_shown = True
                self.phase = Phase.DONE
                self.message = f"Perfecte! Operació acabada. El resultat és {self.num_result}."
                self.message_color = (60, 200, 100)
                self.is_finished = True

            case Phase.DONE:
                pass

    def on_borrow_u_finished(self) -> None:
        self.borrow_u_active = True
        self.phase = Phase.ADD_CARRY_T  
        self.message = f"Portada rebuda! Abans de restar, sumem a sota: {self.digits_b[1]} + 1. Fes clic per veure el canvi."

    def on_borrow_t_finished(self) -> None:
        self.borrow_d_active = True
        self.phase = Phase.ADD_CARRY_H  
        self.message = f"Portada rebuda! Sumem a les centenes inferiors: {self.digits_b[0]} + 1. Fes clic per actualitzar."