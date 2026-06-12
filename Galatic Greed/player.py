import pygame
from ship import Ship

class Player(Ship):
    """
    Handles user-controlled ships with improved visibility,
    forward-only firing logic, and white-freeze visual effects.
    """
    def __init__(self, x, y, color, controls="P1"):
        super().__init__(x, y, color)
        self.controls = controls
        self.score = 0
        self.is_frozen = False
        self.freeze_time = 0
        self.last_shot = 0
        # Increased dimensions for better visibility
        self.width = 35 
        self.height = 45

    def apply_freeze(self):
        """Activates the freeze state and turns the ship pure white."""
        self.is_frozen = True
        self.freeze_time = pygame.time.get_ticks()

    def handle_movement(self, screen_w, screen_h):
        """Processes movement and ensures both players fire forward (Up)."""
        now = pygame.time.get_ticks()
        
        # Freeze Logic
        if self.is_frozen:
            if now - self.freeze_time > 2000: 
                self.is_frozen = False
            else:
                return # Movement and shooting disabled while frozen

        keys = pygame.key.get_pressed()
        
        # Player 1 Controls (WASD + Space)
        if self.controls == "P1":
            if keys[pygame.K_w] and self.y > 0: self.y -= self.speed
            if keys[pygame.K_s] and self.y < screen_h - self.height: self.y += self.speed
            if keys[pygame.K_a] and self.x > 0: self.x -= self.speed
            if keys[pygame.K_d] and self.x < screen_w - self.width: self.x += self.speed
            
            # Fire Forward (Up)
            if keys[pygame.K_SPACE] and now - self.last_shot > 400:
                self.shoot(-1) 
                self.last_shot = now
                
        # Player 2 Controls (Arrows + M)
        else:
            if keys[pygame.K_UP] and self.y > 0: self.y -= self.speed
            if keys[pygame.K_DOWN] and self.y < screen_h - self.height: self.y += self.speed
            if keys[pygame.K_LEFT] and self.x > 0: self.x -= self.speed
            if keys[pygame.K_RIGHT] and self.x < screen_w - self.width: self.x += self.speed
            
            # Fire Forward (Up) - Fixed from backward to forward
            if keys[pygame.K_m] and now - self.last_shot > 400:
                self.shoot(-1) 
                self.last_shot = now

    def draw(self, screen):
        """Renders an upgraded ship design with cockpit and engine details."""
        # Visual feedback: WHITE if frozen, else original team color
        draw_color = (255, 255, 255) if self.is_frozen else self.color
        
        # Main Hull (Triangle)
        pts = [(self.x + self.width // 2, self.y), 
               (self.x, self.y + self.height), 
               (self.x + self.width, self.y + self.height)]
        pygame.draw.polygon(screen, draw_color, pts)
        
        # Cockpit detail for a better look
        cockpit_color = (170, 220, 255) if not self.is_frozen else (200, 200, 200)
        pygame.draw.circle(screen, cockpit_color, (int(self.x + self.width//2), int(self.y + self.height//1.8)), 5)
        
        # Engine Glow (Orange flame effect)
        if not self.is_frozen:
            engine_rect = (self.x + self.width//4, self.y + self.height, self.width//2, 6)
            pygame.draw.rect(screen, (255, 140, 0), engine_rect)
            pygame.draw.rect(screen, (255, 255, 0), (self.x + self.width//3, self.y + self.height, self.width//3, 3))

        # Ammo Indicators (Green dots moved lower to avoid overlapping with engine)
        for i in range(self.bullets):
            pygame.draw.circle(screen, (0, 255, 100), (int(self.x + (i * 7)), int(self.y + self.height + 15)), 3)