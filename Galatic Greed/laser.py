import pygame

class Laser:
    """
    Handles projectile physics and rendering.
    Features a dual-layer drawing method for a neon plasma effect.
    """
    def __init__(self, x, y, color, direction=-1):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction  # -1 for Up (P1), 1 for Down (P2)
        self.speed = 15             # Increased speed for better gameplay feel
        self.width = 4
        self.height = 20            # Slightly longer for better visibility

    def draw(self, screen):
        """
        Renders the laser with a plasma core and a neon outer glow.
        """
        # Outer neon glow layer
        pygame.draw.rect(screen, self.color, (self.x - 2, self.y, self.width + 4, self.height))
        # Bright white plasma core
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

    def move(self):
        """
        Updates the Y-coordinate based on direction and speed.
        """
        self.y += (self.speed * self.direction)

    def off_screen(self, height):
        """
        Checks if the laser has exited the 800x800 game frame.
        """
        return self.y < -20 or self.y > height + 20

    def collision(self, obj):
        """
        Precise AABB collision detection against another game object.
        """
        return (self.x + self.width > obj.x and 
                self.x < obj.x + obj.width and
                self.y + self.height > obj.y and 
                self.y < obj.y + obj.height)