import pygame

class GalacticColors:
    # NASA / JAXA Standard Color Palette
    SPACE_VOID = (5, 5, 20)      # Deep Navy
    SUN_GOLD   = (255, 204, 0)   # Solar standard
    PLAYER_1   = (0, 255, 255)   # Cyan (P1)
    PLAYER_2   = (255, 102, 255) # Magenta (P2)
    ASTEROID   = (128, 128, 128) # Grey
    TREASURE   = (0, 255, 150)   # Neon Green
    TEXT_WHITE = (240, 240, 240) # Off-white
    UI_NAVY    = (15, 15, 35)    # UI Background

class Sprites:
    @staticmethod
    def draw_glow(screen, color, x, y, radius):
        """Adds a professional neon glow to space objects."""
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (*color, 60), (radius, radius), radius)
        screen.blit(surface, (x - radius, y - radius))