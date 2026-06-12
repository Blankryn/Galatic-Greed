import pygame
import random

class Level:
    """
    Generates an immersive deep-space background using parallax star fields 
    and multi-layered nebulae with alpha transparency for a cinematic feel.
    """
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        
        # Parallax Stars (Cinematic depth layers)
        self.stars = []
        for _ in range(180): # Increased star count
            layer = random.choice([1, 2, 3]) 
            self.stars.append([
                random.randint(0, self.width), 
                random.randint(0, self.height),
                layer, 
                layer * 0.3, # Parallax movement speed
                random.randint(100, 255), # Initial brightness
                random.choice([-1, 1]) # Twinkle direction
            ])
            
        # Background Nebulae (Deep space dust clouds)
        # Using NASA/JAXA standards: Deep Violets, Teals, and Indigo
        self.nebulae = []
        # Added Alpha (4th value) for transparency
        colors = [(40, 10, 70, 40), (10, 50, 60, 30), (60, 20, 40, 35)]
        for _ in range(6): 
            self.nebulae.append({
                "pos": (random.randint(0, self.width), random.randint(0, self.height)),
                "color": random.choice(colors),
                "radius": random.randint(200, 450)
            })

    def draw_background(self, screen):
        """Renders the layered celestial environment."""
        # Ultra-dark space base
        screen.fill((5, 5, 15)) 

        # Draw Nebulae with transparency (Surface optimization)
        for n in self.nebulae:
            # Create a transparent surface for the nebula
            neb_surface = pygame.Surface((n["radius"]*2, n["radius"]*2), pygame.SRCALPHA)
            pygame.draw.circle(neb_surface, n["color"], (n["radius"], n["radius"]), n["radius"])
            screen.blit(neb_surface, (n["pos"][0] - n["radius"], n["pos"][1] - n["radius"]))

        # Draw and Animate Parallax Stars
        for star in self.stars:
            # Twinkle Logic: Slowly change brightness
            star[4] += star[5] * 2
            if star[4] > 255 or star[4] < 100:
                star[5] *= -1 # Reverse brightness change
                star[4] = max(100, min(255, star[4]))

            color = (star[4], star[4], star[4])
            pygame.draw.circle(screen, color, (int(star[0]), int(star[1])), star[2])
            
            # Continuous movement based on parallax layer
            star[1] += star[3]
            
            # Reset to top for seamless loop
            if star[1] > self.height:
                star[1] = 0
                star[0] = random.randint(0, self.width)

    def update_level(self, player_score):
        """Dynamic background changes based on game progress."""
        pass