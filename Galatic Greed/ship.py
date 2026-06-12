from laser import Laser

class Ship:
    """
    Base class for all space vessels. 
    Manages position, combat mechanics, and projectile tracking.
    """
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = 7 # Increased speed for better frame coverage
        self.width = 40
        self.height = 40
        self.shots = []
        
        # Ammo Mechanics
        self.bullets = 0    # Starts with 0 ammo as requested
        self.max_ammo = 6   # Maximum ammo capacity is 6
        
    def shoot(self, direction):
        """
        Creates a new laser instance and tracks it.
        Direction: -1 for up, 1 for down.
        """
        if self.bullets > 0:
            # Centering the laser based on ship width
            laser_x = self.x + self.width // 2
            # Laser starting Y depends on which way it is firing
            laser_y = self.y if direction == -1 else self.y + self.height
            
            new_laser = Laser(laser_x, laser_y, self.color, direction)
            self.shots.append(new_laser)
            self.bullets -= 1
        else:
            # Optional: Add a 'no ammo' click sound effect logic here later
            pass

    def move_shots(self, screen, target):
        """
        Updates laser positions and checks for collision with the opponent.
        """
        for s in self.shots[:]:
            s.move()
            
            # Check if laser left the 800x800 frame
            if s.off_screen(screen.get_height()):
                if s in self.shots:
                    self.shots.remove(s)
            
            # Check for collision with target player
            elif s.collision(target):
                target.apply_freeze() # Freezes the hit player
                if s in self.shots:
                    self.shots.remove(s)