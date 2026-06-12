import pygame
import math
import random

# JAXA/NASA inspired palette
COLOR_ASTEROID = (100, 100, 105)
COLOR_MYSTERY_BOX = (255, 215, 0) # Golden yellow for visibility
COLOR_TREASURE = (0, 255, 150)    # Neon Cyan/Green

class Asteroid:
    """Jagged space rocks that subtract points on collision."""
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = random.randint(15, 30) # Slightly larger for better gameplay
        # Create a jagged shape for the asteroid
        self.points = []
        for i in range(8):
            angle = math.radians(i * 45)
            r = self.radius * random.uniform(0.7, 1.3)
            self.points.append((math.cos(angle) * r, math.sin(angle) * r))

    def move(self):
        self.y += self.speed

    def draw(self, screen):
        draw_points = [(self.x + p[0], self.y + p[1]) for p in self.points]
        # Base shadow layer
        pygame.draw.polygon(screen, (40, 40, 45), draw_points)
        # Main body
        pygame.draw.polygon(screen, COLOR_ASTEROID, draw_points, 0)
        # Detailed outline
        pygame.draw.polygon(screen, (150, 150, 160), draw_points, 1)

    def off_screen(self, height):
        return self.y > height + 50

class CelestialBody:
    """Planets and Moons that orbit a center point for a dynamic map."""
    def __init__(self, name, distance, speed, radius, color, has_rings=False, parent=None):
        self.name = name
        self.distance = distance
        self.speed = speed
        self.radius = radius
        self.color = color
        self.has_rings = has_rings
        self.angle = random.uniform(0, 2 * math.pi)
        self.parent = parent
        self.x, self.y = 0, 0

    def update(self, center_x, center_y):
        self.angle += self.speed
        origin_x = self.parent.x if self.parent else center_x
        origin_y = self.parent.y if self.parent else center_y
        self.x = origin_x + math.cos(self.angle) * self.distance
        self.y = origin_y + math.sin(self.angle) * self.distance

    def draw(self, screen):
        # Orbit Path
        origin_pos = (int(self.parent.x), int(self.parent.y)) if self.parent else (400, 400)
        pygame.draw.circle(screen, (30, 30, 60), origin_pos, int(self.distance), 1)
        
        # Rings (Optional)
        if self.has_rings:
            rect = (self.x - self.radius*2, self.y - self.radius//2, self.radius*4, self.radius)
            pygame.draw.ellipse(screen, (120, 120, 150), rect, 2)
            
        # Planet Body
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # High-altitude atmosphere glow
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x - self.radius//3), int(self.y - self.radius//3)), self.radius//4)

class MysteryBox:
    """Supply boxes that reload ammo (Updated for Max 6 ammo capacity)."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 22
        self.pulse = 0

    def draw(self, screen):
        self.pulse += 0.15
        current_size = self.size + math.sin(self.pulse) * 4
        rect = pygame.Rect(self.x - current_size//2, self.y - current_size//2, current_size, current_size)
        
        # Outer Glow
        pygame.draw.rect(screen, (255, 255, 255), rect.inflate(4, 4), 1)
        # Box Body
        pygame.draw.rect(screen, COLOR_MYSTERY_BOX, rect)
        
        # Ammo Icon Label
        font = pygame.font.SysFont('Arial', 14, bold=True)
        label = font.render("AMMO", True, (0, 0, 0))
        label_rect = label.get_rect(center=(self.x, self.y))
        screen.blit(label, label_rect)