import pygame
import sys
import os
from player import Player
from celestial_manager import HazardManager
from level import Level

# Force the window to spawn slightly higher on the screen
os.environ['SDL_VIDEO_WINDOW_POS'] = "center,30"

# Initialize Pygame
pygame.init()

# Constants - Height reduced to 750 to sit above most taskbars
WIDTH, HEIGHT = 850, 750 
FPS = 60
WHITE = (220, 220, 220)
CYAN = (0, 255, 255)
GOLD = (255, 215, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Greed")
clock = pygame.time.Clock()

# Space-themed fonts
title_font = pygame.font.SysFont("Verdana", 50, bold=True)
header_font = pygame.font.SysFont("Verdana", 28, bold=True)
ui_font = pygame.font.SysFont("Courier New", 20, bold=True)

def draw_text(text, x, y, color=WHITE, font_type=ui_font, center=False):
    """Refined text rendering for a better UI feel."""
    surface = font_type.render(text, True, color)
    rect = surface.get_rect(center=(x, y)) if center else surface.get_rect(topleft=(x, y))
    screen.blit(surface, rect)

def show_result(p1_score, p2_score):
    """Displays the mission summary and determines the winner."""
    while True:
        screen.fill((5, 5, 25))
        draw_text("MISSION SUMMARY", WIDTH//2, 150, GOLD, title_font, True)
        
        if p1_score > p2_score:
            res_msg = f"PLAYER 1 DOMINATES! ({p1_score} pts)"
            res_col = (0, 200, 255)
        elif p2_score > p1_score:
            res_msg = f"PLAYER 2 DOMINATES! ({p2_score} pts)"
            res_col = (255, 80, 80)
        else:
            res_msg = f"STALEMATE - DRAW! ({p1_score} pts)"
            res_col = WHITE
            
        draw_text(res_msg, WIDTH//2, 300, res_col, header_font, True)
        draw_text(f"P1 Total: {p1_score} | P2 Total: {p2_score}", WIDTH//2, 400, WHITE, ui_font, True)
        draw_text("Press [B] to Return to Command Center", WIDTH//2, 550, (180, 180, 180), ui_font, True)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                return

def instruction_screen():
    """Detailed manual for the mission."""
    while True:
        screen.fill((5, 5, 15))
        draw_text("Mission Manual", WIDTH//2, 80, CYAN, header_font, True)
        
        guide = [
            "P1 Controls: [W,A,S,D] to pilot | [Space] to fire",
            "P2 Controls: [Arrows] to pilot | [M] to fire",
            "",
            "Core Mechanics:",
            "- Both ships fire Forward (Upward).",
            "- Ammo: Starts at 0. Max capacity is 6.",
            "- Freeze: Laser hits turn opponent WHITE for 2s.",
            "- Resupply: Collect golden Mystery Boxes (+2 ammo).",
            "- Black Hole: Every minute for 10s. Hit = -10 pts.",
            "- Treasures: Collect neon orbs for +5 points.",
            "",
            "Press [B] to return to Main Menu"
        ]
        
        for i, line in enumerate(guide):
            draw_text(line, WIDTH//2, 160 + (i * 35), WHITE, ui_font, True)
            
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                return

def main_menu():
    """The landing page with duration selection."""
    while True:
        screen.fill((2, 2, 15))
        draw_text("GALACTIC GREED", WIDTH//2, 150, GOLD, title_font, True)
        draw_text("Select Mission Duration", WIDTH//2, 280, WHITE, header_font, True)
        
        durations = {pygame.K_2: 120, pygame.K_5: 300, pygame.K_8: 480, pygame.K_0: 600}
        draw_text("[2] 2 Mins  |  [5] 5 Mins", WIDTH//2, 360, CYAN, ui_font, True)
        draw_text("[8] 8 Mins  |  [0] 10 Mins", WIDTH//2, 400, CYAN, ui_font, True)
        
        draw_text("Press [H] for Help  |  Press [Q] to Quit", WIDTH//2, 550, (200, 200, 200), ui_font, True)
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()
                if event.key == pygame.K_h:
                    instruction_screen()
                if event.key in durations:
                    return durations[event.key]

def run_game(duration):
    """Active mission execution."""
    # Start ships higher from the bottom edge
    p1 = Player(200, HEIGHT - 120, (0, 200, 255), "P1")
    p2 = Player(WIDTH - 250, HEIGHT - 120, (255, 80, 80), "P2")
    hazards = HazardManager(WIDTH, HEIGHT)
    level_bg = Level(WIDTH, HEIGHT)
    
    start_ticks = pygame.time.get_ticks()
    
    while True:
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, duration - seconds_passed)
        
        if time_left == 0:
            show_result(p1.score, p2.score)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                return

        # Update Logic
        p1.handle_movement(WIDTH, HEIGHT)
        p2.handle_movement(WIDTH, HEIGHT)

        # Force Boundary Check: Prevents ship from going below 60px from the bottom
        for p in [p1, p2]:
            if p.y > HEIGHT - 70:
                p.y = HEIGHT - 70

        p1.move_shots(screen, p2)
        p2.move_shots(screen, p1)
        hazards.update(p1, p2, time_left)

        # Draw Sequence
        level_bg.draw_background(screen)
        hazards.draw(screen)
        p1.draw(screen)
        p2.draw(screen)
        
        for s in p1.shots + p2.shots: s.draw(screen)

        # HUD
        draw_text(f"P1: {p1.score}", 20, 20, p1.color, ui_font)
        draw_text(f"P2: {p2.score}", WIDTH - 120, 20, p2.color, ui_font)
        draw_text(f"Time: {time_left}s", WIDTH // 2 - 50, 20, WHITE, ui_font)
        draw_text("Press [B] for Menu", WIDTH // 2, HEIGHT - 30, (150, 150, 150), ui_font, True)
        
        if hazards.event_active:
            draw_text("Warning: Spatial Distortion (Black Hole Wave)", WIDTH // 2, HEIGHT - 80, (180, 0, 255), ui_font, True)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    while True:
        mission_time = main_menu()
        run_game(mission_time)