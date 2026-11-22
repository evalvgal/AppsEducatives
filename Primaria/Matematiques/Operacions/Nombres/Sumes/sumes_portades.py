"""
Suma amb Portades — Model lògic, dades i càlculs de sumes.
"""

import random
from enum import Enum, auto

class Phase(Enum):
    INPUT        = auto()   
    STEP_UNITS   = auto()   # sumant unitats, esperant veure la suma total a sota
    SHOW_TOTAL_U = auto()   # mostra el nombre de dues xifres a sota (ex: 12)
    ANIM_CARRY_U = auto()   # animant la portada de U a D
    STEP_TENS    = auto()   # sumant desenes, esperant veure la suma total a sota
    SHOW_TOTAL_D = auto()   # mostra el nombre de dues xifres a sota a les desenes
    ANIM_CARRY_T = auto()   # animant la portada de D a C
    STEP_HUNDS   = auto()   # sumant centenes
    DONE         = auto()   # resultat final

class SumaModel:
    def __init__(self) -> None:
        self.new_problem()

    def new_problem(self) -> None:
        while True:
            a = random.randint(10, 499)
            b = random.randint(10, 499)
            au, bu = a % 10, b % 10
            ad, bd = (a // 10) % 10, (b // 10) % 10
            if (au + bu >= 10) or (ad + bd >= 10):
                break

        self.num_a = a
        self.num_b = b
        self.num_result = a + b

        self.a_h  = a // 100
        self.a_d  = (a // 10) % 10
        self.a_u  = a % 10
        self.b_h  = b // 100
        self.b_d  = (b // 10) % 10
        self.b_u  = b % 10

        self.sum_u   = self.a_u + self.b_u
        self.carry_u = self.sum_u // 10          
        self.digit_u = self.sum_u % 10

        self.sum_d   = self.a_d + self.b_d + self.carry_u
        self.carry_d = self.sum_d // 10          
        self.digit_d = self.sum_d % 10

        self.sum_h   = self.a_h + self.b_h + self.carry_d
        self.digit_h = self.sum_h % 10
        self.extra_h = self.sum_h // 10          

        self.phase: Phase = Phase.STEP_UNITS
        self.carry_u_shown: bool = False    
        self.carry_d_shown: bool = False    
        self.result_u_shown: bool = False
        self.result_d_shown: bool = False
        self.result_h_shown: bool = False

        self.message: str = "¡Comencem sumant les UNITATS!"
        self.is_finished: bool = False
        self.need_anim_u: bool = False
        self.need_anim_t: bool = False

    def advance_step(self) -> None:
        self.need_anim_u = False
        self.need_anim_t = False

        match self.phase:
            case Phase.STEP_UNITS:
                self.result_u_shown = True
                if self.carry_u > 0:
                    self.phase = Phase.SHOW_TOTAL_U
                    self.message = f"{self.a_u} + {self.b_u} = {self.sum_u}. És més gran que 9! Escrivim el {self.sum_u} sencer a sota de moment."
                else:
                    self.phase   = Phase.STEP_TENS
                    self.message = f"{self.a_u} + {self.b_u} = {self.digit_u}  |  Ara sumem les DESENES."

            case Phase.SHOW_TOTAL_U:
                self.phase = Phase.ANIM_CARRY_U
                self.message = f"¡L'1 es cansa d'estar a sota i viatja volant cap a les Desenes!"
                self.need_anim_u = True

            case Phase.ANIM_CARRY_U:
                pass

            case Phase.STEP_TENS:
                self.result_d_shown = True
                extra = f" + {self.carry_u} (de portada)" if self.carry_u else ""
                if self.carry_d > 0:
                    self.phase = Phase.SHOW_TOTAL_D
                    self.message = f"{self.a_d} + {self.b_d}{extra} = {self.sum_d}. ¡Hi posem el {self.sum_d} provisionalment!"
                else:
                    self.phase   = Phase.STEP_HUNDS
                    self.message = f"{self.a_d} + {self.b_d}{extra} = {self.digit_d}  |  ¡Ara les CENTENES!"

            case Phase.SHOW_TOTAL_D:
                self.phase = Phase.ANIM_CARRY_T
                self.message = f"¡L'1 vola cap a la columna de les Centenes!"
                self.need_anim_t = True

            case Phase.ANIM_CARRY_T:
                pass

            case Phase.STEP_HUNDS:
                self.result_h_shown = True
                self.phase = Phase.DONE
                self.message = f"¡Resultat final: {self.num_a} + {self.num_b} = {self.num_result}!"
                self.is_finished = True

            case Phase.DONE:
                pass

    def on_carry_u_finished(self) -> None:
        self.carry_u_shown = True
        self.phase = Phase.STEP_TENS
        self.message = "La portada 1 ja és a la seva casella. ¡Sumem les DESENES!"

    def on_carry_t_finished(self) -> None:
        self.carry_d_shown = True
        self.phase = Phase.STEP_HUNDS
        self.message = "La portada 1 ja és a la seva casella. ¡Sumem les CENTENES!"