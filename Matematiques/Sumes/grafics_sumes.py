"""
Suma amb Portades — Interfície gràfica i bucle principal amb Pygame.
Requeriments: pip install pygame
Executar: python grafics.py
"""

import sys
import math
import random
import pygame
from dataclasses import dataclass, field
from sumes_portades import SumaModel, Phase

# ─────────────────────────── Constants globals ────────────────────────────

FPS          = 60
WIN_W, WIN_H = 900, 720  # Resolució lògica de disseny
TITLE        = "Suma amb Portades"

# Paleta de colors (suaus, no saturats)
BG           = (245, 242, 255)
C_COL_BG     = (255, 228, 196)   # préssec — Centenes
D_COL_BG     = (196, 228, 255)   # blau cel — Desenes
U_COL_BG     = (196, 255, 210)   # menta    — Unitats
C_COL_BD     = (230, 170, 120)
D_COL_BD     = (120, 170, 230)
U_COL_BD     = (100, 210, 140)

TEXT_DARK    = (50,  40,  80)
TEXT_MID     = (110, 100, 140)
TEXT_WHITE   = (255, 255, 255)
CARRY_COLOR  = (255,  80,  80)   # vermell cridaner per a la portada
CARRY_BG     = (255, 220, 220)
BTN_MAIN     = ( 90, 160, 255)
BTN_HOVER    = ( 60, 130, 230)
BTN_NEW      = (100, 210, 120)
BTN_NEW_HOV  = ( 70, 180,  90)
GREEN_OK     = ( 60, 200, 100)
RED_ERR      = (230,  70,  70)

# Geometria de la quadrícula redistribuïda (Centenes, Desenes, Unitats)
GRID_TOP     = 210  
GRID_H       = 320  
COL_W        = 180
COL_GAP      = 12
GRID_LEFT    = (WIN_W - (3 * COL_W + 2 * COL_GAP)) // 2
CARRY_R      = 24   
CARRY_Y      = GRID_TOP - 45  


@dataclass
class CarryAnimation:
    """Partícula que viatja des de la columna origen cap a la casella de la portada."""
    start_x:  float
    start_y:  float
    end_x:    float
    end_y:    float
    digit:    int
    progress: float = 0.0          
    speed:    float = 0.020        
    done:     bool  = False

    def update(self) -> None:
        self.progress = min(1.0, self.progress + self.speed)
        if self.progress >= 1.0:
            self.done = True

    @property
    def current_pos(self) -> tuple[float, float]:
        t = 1 - (1 - self.progress) ** 3
        cx = self.start_x + (self.end_x - self.start_x) * t
        cy = self.start_y + (self.end_y - self.start_y) * t - 120 * math.sin(math.pi * t)
        return cx, cy

    @property
    def current_alpha(self) -> int:
        return int(255 * min(1.0, self.progress * 4))

    @property
    def current_scale(self) -> float:
        t = 1 - (1 - self.progress) ** 3
        return 0.8 + 0.2 * t


@dataclass
class Button:
    rect:      pygame.Rect
    text:      str
    color:     tuple[int, int, int]
    hover_col: tuple[int, int, int]
    enabled:   bool = True
    _hovered:  bool = field(default=False, repr=False)

    def update(self, mouse_pos: tuple[int, int]) -> None:
        self._hovered = self.rect.collidepoint(mouse_pos) and self.enabled

    def clicked(self, mouse_pos: tuple[int, int], event: pygame.event.Event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(mouse_pos)
                and self.enabled)

    def draw(self, surf: pygame.Surface, font: pygame.font.Font) -> None:
        col = self.hover_col if self._hovered else self.color
        if not self.enabled:
            col = tuple(min(255, c + 60) for c in self.color)  # type: ignore[arg-type]
        pygame.draw.rect(surf, col, self.rect, border_radius=14)
        pygame.draw.rect(surf, TEXT_DARK, self.rect, 2, border_radius=14)
        txt = font.render(self.text, True, TEXT_WHITE)
        surf.blit(txt, txt.get_rect(center=self.rect.center))


def col_center_x(col_index: int) -> int:
    return GRID_LEFT + col_index * (COL_W + COL_GAP) + COL_W // 2


def draw_rounded_rect_with_border(
    surf: pygame.Surface,
    rect: pygame.Rect,
    fill: tuple[int, int, int],
    border: tuple[int, int, int],
    radius: int = 16,
    border_width: int = 3
) -> None:
    pygame.draw.rect(surf, fill, rect, border_radius=radius)
    pygame.draw.rect(surf, border, rect, border_width, border_radius=radius)


def draw_text_centered(
    surf: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    cx: int,
    cy: int,
    alpha: int = 255
) -> None:
    if alpha < 255:
        tmp = font.render(text, True, color)
        tmp.set_alpha(alpha)
        surf.blit(tmp, tmp.get_rect(center=(cx, cy)))
    else:
        rendered = font.render(text, True, color)
        surf.blit(rendered, rendered.get_rect(center=(cx, cy)))


def make_star_positions(n: int, area: pygame.Rect) -> list[tuple[int, int]]:
    return [(random.randint(area.left, area.right),
             random.randint(area.top, area.bottom)) for _ in range(n)]


class SumaPortadesApp:

    def __init__(self) -> None:
        pygame.init()
        
        info_pantalla = pygame.display.Info()
        ancho_pantalla_disponible = info_pantalla.current_w
        alto_pantalla_disponible = info_pantalla.current_h

        ancho_ventana = min(WIN_W, int(ancho_pantalla_disponible * 0.85))
        alto_ventana = min(WIN_H, int(alto_pantalla_disponible * 0.80))

        proporcion = WIN_W / WIN_H
        if ancho_ventana / alto_ventana > proporcion:
            ancho_ventana = int(alto_ventana * proporcion)
        else:
            alto_ventana = int(ancho_ventana / proporcion)

        self.screen_real = pygame.display.set_mode((ancho_ventana, alto_ventana), pygame.RESIZABLE)
        self.screen = pygame.Surface((WIN_W, WIN_H))
        
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self._load_fonts()
        self._build_ui()
        
        self.model = SumaModel()
        self.animations: list[CarryAnimation] = []
        self._confetti: list[dict] = []
        self._stars = make_star_positions(30, pygame.Rect(0, 0, WIN_W, WIN_H // 2))

    def _get_mouse_pos_logical(self) -> tuple[int, int]:
        pos_real = pygame.mouse.get_pos()
        w_real, h_real = self.screen_real.get_size()
        x = int(pos_real[0] * (WIN_W / w_real)) if w_real > 0 else 0
        y = int(pos_real[1] * (WIN_H / h_real)) if h_real > 0 else 0
        return (x, y)

    def _load_fonts(self) -> None:
        def try_font(names: list[str], size: int) -> pygame.font.Font:
            for name in names:
                try:
                    f = pygame.font.SysFont(name, size, bold=True)
                    return f
                except Exception:
                    pass
            return pygame.font.Font(None, size)

        self.font_title  = try_font(["comicsansms", "chalkboard", "arial"], 38)
        self.font_big    = try_font(["comicsansms", "chalkboard", "arial"], 54)
        self.font_medium = try_font(["comicsansms", "chalkboard", "arial"], 36)
        self.font_small  = try_font(["comicsansms", "chalkboard", "arial"], 26)
        self.font_label  = try_font(["comicsansms", "chalkboard", "arial"], 20)

    def _build_ui(self) -> None:
        bw, bh = 220, 52
        margin = 24
        total_btns_w = 2 * bw + margin
        bx = (WIN_W - total_btns_w) // 2
        by = WIN_H - 75

        self.btn_step = Button(
            rect      = pygame.Rect(bx, by, bw, bh),
            text      = "Pas següent",
            color     = BTN_MAIN,
            hover_col = BTN_HOVER,
        )
        self.btn_new = Button(
            rect      = pygame.Rect(bx + bw + margin, by, bw, bh),
            text      = "Nou problema",
            color     = BTN_NEW,
            hover_col = BTN_NEW_HOV,
        )

    def _new_problem(self) -> None:
        self.model.new_problem()
        self.animations = []
        self._confetti = []
        self.btn_step.enabled = True

    def _advance_step(self) -> None:
        result_y = GRID_TOP + 288
        self.model.advance_step()

        if self.model.need_anim_u:
            src_x = col_center_x(2) - 15
            self._launch_carry_anim(src_x=src_x, src_y=result_y, dst_col=1, digit=self.model.carry_u)
        elif self.model.need_anim_t:
            src_x = col_center_x(1) - 15
            self._launch_carry_anim(src_x=src_x, src_y=result_y, dst_col=0, digit=self.model.carry_d)
        elif self.model.is_finished:
            self._confetti = self._make_confetti(60)
            self.btn_step.enabled = False

    def _launch_carry_anim(self, src_x: float, src_y: float, dst_col: int, digit: int) -> None:
        ex = float(col_center_x(dst_col))
        ey = float(CARRY_Y)
        self.animations.append(
            CarryAnimation(start_x=src_x, start_y=src_y, end_x=ex, end_y=ey, digit=digit)
        )
        self.btn_step.enabled = False

    def _update_animations(self) -> None:
        for anim in self.animations:
            anim.update()

        finished = [a for a in self.animations if a.done]
        if finished:
            self.animations = [a for a in self.animations if not a.done]
            if self.model.phase == Phase.ANIM_CARRY_U:
                self.model.on_carry_u_finished()
                self.btn_step.enabled = True
            elif self.model.phase == Phase.ANIM_CARRY_T:
                self.model.on_carry_t_finished()
                self.btn_step.enabled = True

    def _make_confetti(self, n: int) -> list[dict]:
        colors = [(255, 80, 80), (80, 200, 80), (80, 80, 255), (255, 200, 0)]
        particles = []
        for _ in range(n):
            particles.append({
                "x":  random.uniform(0, WIN_W),
                "y":  random.uniform(-80, 0),
                "vy": random.uniform(2.5, 5.5),
                "vx": random.uniform(-1.5, 1.5),
                "w":  random.randint(8, 18),
                "h":  random.randint(6, 12),
                "col": random.choice(colors),
                "rot": random.uniform(0, 360),
                "drot": random.uniform(-6, 6),
            })
        return particles

    def _update_confetti(self) -> None:
        for p in self._confetti:
            p["x"]   += p["vx"]
            p["y"]   += p["vy"]
            p["rot"] += p["drot"]
        self._confetti = [p for p in self._confetti if p["y"] < WIN_H + 30]

    def _draw_confetti(self, surf: pygame.Surface) -> None:
        for p in self._confetti:
            tmp = pygame.Surface((p["w"], p["h"]), pygame.SRCALPHA)
            tmp.fill((*p["col"], 210))
            rotated = pygame.transform.rotate(tmp, p["rot"])
            surf.blit(rotated, rotated.get_rect(center=(int(p["x"]), int(p["y"]))))

    def _draw_background(self, surf: pygame.Surface) -> None:
        surf.fill(BG)
        for sx, sy in self._stars:
            pygame.draw.circle(surf, (220, 215, 240), (sx, sy), 2)

    def _draw_header(self, surf: pygame.Surface) -> None:
        draw_text_centered(surf, "Suma amb Portades", self.font_title, TEXT_DARK, WIN_W // 2, 35)
        num_str = f"{self.model.num_a}  +  {self.model.num_b}  =  ?"
        draw_text_centered(surf, num_str, self.font_medium, TEXT_MID, WIN_W // 2, 85)

    def _draw_columns(self, surf: pygame.Surface) -> None:
        col_data = [
            (0, "C", C_COL_BG, C_COL_BD, "Centenes"),
            (1, "D", D_COL_BG, D_COL_BD, "Desenes"),
            (2, "U", U_COL_BG, U_COL_BD, "Unitats"),
        ]
        for idx, letter, bg, bd, label in col_data:
            rx = GRID_LEFT + idx * (COL_W + COL_GAP)
            ry = GRID_TOP
            rect = pygame.Rect(rx, ry, COL_W, GRID_H)
            draw_rounded_rect_with_border(surf, rect, bg, bd)
            draw_text_centered(surf, label,  self.font_label, bd, rx + COL_W // 2, ry + 24)
            draw_text_centered(surf, letter, self.font_big,   bd, rx + COL_W // 2, ry + 65)

    def _draw_numbers_in_columns(self, surf: pygame.Surface) -> None:
        digits_a = [self.model.a_h, self.model.a_d, self.model.a_u]
        digits_b = [self.model.b_h, self.model.b_d, self.model.b_u]
        for col in range(3):
            cx = col_center_x(col)
            if digits_a[col] > 0 or col > 0:
                draw_text_centered(surf, str(digits_a[col]), self.font_big, TEXT_DARK, cx, GRID_TOP + 130)
            draw_text_centered(surf, "+", self.font_medium, TEXT_MID, cx - COL_W // 2 + 22, GRID_TOP + 165)
            if digits_b[col] > 0 or col > 0:
                draw_text_centered(surf, str(digits_b[col]), self.font_big, TEXT_DARK, cx, GRID_TOP + 200)

        line_y = GRID_TOP + 250
        lx = GRID_LEFT + 10
        pygame.draw.line(surf, TEXT_MID, (lx, line_y), (lx + 3 * COL_W + 2 * COL_GAP - 20, line_y), 4)

    def _draw_results(self, surf: pygame.Surface) -> None:
        result_y = GRID_TOP + 288
        
        if self.model.result_u_shown:
            if self.model.phase == Phase.SHOW_TOTAL_U:
                draw_text_centered(surf, str(self.model.sum_u), self.font_big, RED_ERR, col_center_x(2), result_y)
            else:
                draw_text_centered(surf, str(self.model.digit_u), self.font_big, GREEN_OK, col_center_x(2), result_y)
                
        if self.model.result_d_shown:
            if self.model.phase == Phase.SHOW_TOTAL_D:
                draw_text_centered(surf, str(self.model.sum_d), self.font_big, RED_ERR, col_center_x(1), result_y)
            else:
                draw_text_centered(surf, str(self.model.digit_d), self.font_big, GREEN_OK, col_center_x(1), result_y)
                
        if self.model.result_h_shown:
            digit_str = str(self.model.digit_h)
            if self.model.extra_h:
                digit_str = str(self.model.extra_h) + digit_str
            draw_text_centered(surf, digit_str, self.font_big, GREEN_OK, col_center_x(0), result_y)

    def _draw_carry_boxes(self, surf: pygame.Surface) -> None:
        for col_idx, shown, carry_val in [
            (1, self.model.carry_u_shown, self.model.carry_u),
            (0, self.model.carry_d_shown, self.model.carry_d),
        ]:
            cx = col_center_x(col_idx)
            cy = CARRY_Y
            fill = CARRY_BG if shown and carry_val else (240, 240, 240)
            bd   = CARRY_COLOR if shown and carry_val else TEXT_MID
            pygame.draw.circle(surf, fill, (cx, cy), CARRY_R)
            pygame.draw.circle(surf, bd,   (cx, cy), CARRY_R, 3)
            if shown and carry_val:
                draw_text_centered(surf, str(carry_val), self.font_medium, CARRY_COLOR, cx, cy)
            else:
                draw_text_centered(surf, "?", self.font_small, TEXT_MID, cx, cy)

        for col_idx in (0, 1):
            cx = col_center_x(col_idx)
            draw_text_centered(surf, "portada", self.font_label, TEXT_MID, cx, CARRY_Y - CARRY_R - 12)

    def _draw_animations(self, surf: pygame.Surface) -> None:
        for anim in self.animations:
            px, py = anim.current_pos
            alpha  = anim.current_alpha
            scale  = anim.current_scale
            r      = int(CARRY_R * scale)
            
            shadow_surf = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(shadow_surf, (0, 0, 0, 40), (r + 2, r + 2), r)
            surf.blit(shadow_surf, (int(px) - r - 2, int(py) - r - 2))
            
            tmp = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(tmp, (*CARRY_BG, alpha), (r, r), r)
            pygame.draw.circle(tmp, (*CARRY_COLOR, alpha), (r, r), r, 3)
            surf.blit(tmp, (int(px) - r, int(py) - r))
            
            digit_surf = self.font_medium.render(str(anim.digit), True, CARRY_COLOR)
            digit_surf.set_alpha(alpha)
            surf.blit(digit_surf, digit_surf.get_rect(center=(int(px), int(py))))

    def _draw_message(self, surf: pygame.Surface) -> None:
        msg_rect = pygame.Rect(40, WIN_H - 150, WIN_W - 80, 52)
        pygame.draw.rect(surf, (255, 255, 255, 180), msg_rect, border_radius=12)
        pygame.draw.rect(surf, TEXT_MID, msg_rect, 2, border_radius=12)
        
        words = self.model.message.split()
        line, lines = "", []
        for w in words:
            test = f"{line} {w}".strip()
            if self.font_small.size(test)[0] < msg_rect.w - 20:
                line = test
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
        for i, ln in enumerate(lines[:2]):
            col = GREEN_OK if self.model.phase == Phase.DONE else TEXT_DARK
            draw_text_centered(surf, ln, self.font_small, col,
                               WIN_W // 2, msg_rect.centery + (i - (len(lines) - 1) / 2) * 26)

    def _draw_step_indicator(self, surf: pygame.Surface) -> None:
        highlight_map: dict[Phase, int] = {
            Phase.STEP_UNITS:   2,
            Phase.SHOW_TOTAL_U: 2,
            Phase.ANIM_CARRY_U: 2,
            Phase.STEP_TENS:    1,
            Phase.SHOW_TOTAL_D: 1,
            Phase.ANIM_CARRY_T: 1,
            Phase.STEP_HUNDS:   0,
        }
        col_idx = highlight_map.get(self.model.phase)
        if col_idx is not None:
            cx = col_center_x(col_idx)
            pulse = 0.5 + 0.5 * math.sin(pygame.time.get_ticks() * 0.005)
            alpha = int(60 + 60 * pulse)
            hl = pygame.Surface((COL_W - 10, GRID_H - 10), pygame.SRCALPHA)
            hl.fill((255, 255, 100, alpha))
            x = GRID_LEFT + col_idx * (COL_W + COL_GAP) + 5
            surf.blit(hl, (x, GRID_TOP + 5))

    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick(FPS)
            
            mouse_pos_logical = self._get_mouse_pos_logical()
            self.btn_step.update(mouse_pos_logical)
            self.btn_new.update(mouse_pos_logical)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.btn_step.clicked(mouse_pos_logical, event):
                        self._advance_step()
                    if self.btn_new.clicked(mouse_pos_logical, event):
                        self._new_problem()

            self._update_animations()
            if self._confetti:
                self._update_confetti()

            surf = self.screen
            self._draw_background(surf)
            self._draw_header(surf)
            self._draw_step_indicator(surf)
            self._draw_columns(surf)
            self._draw_numbers_in_columns(surf)
            self._draw_carry_boxes(surf)
            self._draw_results(surf)
            self._draw_animations(surf)
            self._draw_message(surf)
            self.btn_step.draw(surf, self.font_small)
            self.btn_new.draw(surf, self.font_small)

            if self._confetti:
                self._draw_confetti(surf)

            self.screen_real.blit(pygame.transform.smoothscale(self.screen, self.screen_real.get_size()), (0, 0))
            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = SumaPortadesApp()
    app.run()