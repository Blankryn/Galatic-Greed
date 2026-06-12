import pygame
import random
import math 
from celestial import Asteroid, CelestialBody, MysteryBox

class HazardManager:
    """
    Manages dynamic environment assets including planets, collectibles, 
    asteroids, and the timed Black Hole event waves.
    """
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        
        # Dynamic Galaxy Setup: Randomly placing planets for a fresh feel
        self.planets = [
            CelestialBody("Jovian", random.randint(140, 180), 0.008, 30, (180, 130, 70), has_rings=True),
            CelestialBody("Ice Giant", random.randint(240, 280), 0.005, 25, (100, 200, 255)),
            CelestialBody("Red Dwarf", random.randint(340, 380), 0.003, 20, (200, 50, 50))
        ]
        self.planets.append(CelestialBody("Moon", 60, 0.04, 8, (200, 200, 200), parent=self.planets[0]))

        self.asteroids = []
        self.treasures = []
        self.mystery_boxes = []
        self.black_holes = []
        
        self.spawn_timer = 0
        self.box_timer = 0
        self.event_active = False

    def spawn_assets(self):
        """Spawns score treasures and ammo boxes with specific limits."""
        # Spawn Treasures (Score) - Max 5 on screen
        if len(self.treasures) < 5:
            self.treasures.append([random.randint(50, self.width-50), random.randint(50, self.height-50)])
        
        # Spawn Mystery Box (Ammo) - Appears periodically
        self.box_timer += 1
        if self.box_timer > 400 and len(self.mystery_boxes) < 2:
            self.mystery_boxes.append(MysteryBox(random.randint(100, self.width-100), random.randint(100, self.height-100)))
            self.box_timer = 0

    def trigger_black_hole_wave(self, active):
        """Manages the spawning and removal of Black Hole hazards during events."""
        self.event_active = active
        if active and len(self.black_holes) == 0:
            # Spawn 3 Black Holes in random quadrants
            for _ in range(3):
                self.black_holes.append({
                    "pos": [random.randint(100, self.width-100), random.randint(100, self.height-100)],
                    "radius": 40,
                    "pulse": 0
                })
        elif not active:
            self.black_holes.clear()

    def update(self, p1, p2, time_left):
        """Updates all hazards, movements, and checks for player collisions."""
        # 1. Handle Black Hole Wave Timing (Every 60s for 10s duration)
        # Assuming duration is in seconds (e.g., 120, 119, 118...)
        if time_left > 0 and time_left % 60 <= 10 and time_left % 60 > 0:
            self.trigger_black_hole_wave(True)
        else:
            self.trigger_black_hole_wave(False)

        # 2. Update Planet Orbits
        for p in self.planets:
            p.update(self.width // 2, self.height // 2)

        # 3. Asteroid Movement and Collision
        self.spawn_timer += 1
        if self.spawn_timer > 60:
            self.asteroids.append(Asteroid(random.randint(0, self.width), -30, random.randint(3, 6)))
            self.spawn_timer = 0

        for a in self.asteroids[:]:
            a.move()
            for p in [p1, p2]:
                if math.hypot(a.x - (p.x + 20), a.y - (p.y + 20)) < (a.radius + 15):
                    p.score = max(0, p.score - 1)
                    if a in self.asteroids: self.asteroids.remove(a)
                    break 
            if a.off_screen(self.height) and a in self.asteroids:
                self.asteroids.remove(a)

        # 4. Black Hole Interaction (-10 Points)
        if self.event_active:
            for bh in self.black_holes:
                bh["pulse"] = (bh["pulse"] + 0.1) % (math.pi * 2)
                for p in [p1, p2]:
                    if math.hypot(bh["pos"][0] - (p.x + 20), bh["pos"][1] - (p.y + 20)) < 50:
                        p.score = max(0, p.score - 10)
                        # Repel player slightly
                        p.x += random.choice([-20, 20])
                        p.y += random.choice([-20, 20])

        self.spawn_assets()

        # 5. Score Treasure Collection (+5 Points)
        for t in self.treasures[:]:
            for p in [p1, p2]:
                if math.hypot(t[0] - (p.x + 20), t[1] - (p.y + 20)) < 30:
                    p.score += 5
                    self.treasures.remove(t)
                    break

        # 6. Mystery Box Collection (Ammo Max 6)
        for box in self.mystery_boxes[:]:
            for p in [p1, p2]:
                if math.hypot(box.x - (p.x + 20), box.y - (p.y + 20)) < 30:
                    p.bullets = min(6, p.bullets + 2) # Adding 2 ammo per box, max 6
                    self.mystery_boxes.remove(box)
                    break

    def draw(self, screen):
        """Draws all celestial objects and hazards with visual effects."""
        for p in self.planets: p.draw(screen)
        
        # Draw Black Holes with pulsing event effect
        for bh in self.black_holes:
            glow = int(15 + math.sin(bh["pulse"]) * 10)
            pygame.draw.circle(screen, (50, 0, 100), bh["pos"], bh["radius"] + glow, 2)
            pygame.draw.circle(screen, (0, 0, 0), bh["pos"], bh["radius"])
            pygame.draw.circle(screen, (150, 0, 255), bh["pos"], bh["radius"] - 5, 1)

        for a in self.asteroids: a.draw(screen)
        for box in self.mystery_boxes: box.draw(screen)
        for t in self.treasures:
            pygame.draw.circle(screen, (0, 255, 150), (t[0], t[1]), 8)
            pygame.draw.circle(screen, (255, 255, 255), (t[0], t[1]), 3)