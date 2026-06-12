# 🌌 Galactic Greed

A fully functional, competitive 2D local multiplayer space shooter game developed in Python using the Pygame graphics library. This project was built as part of the **CSE412/422: Computer Graphics Lab** course at **Daffodil International University**.

The game seamlessly bridges mathematical theory and real-time visual rendering, achieving a smooth **60 FPS performance** with no external graphical assets.

---

## 🚀 Key Features

* **Competitive Local Multiplayer:** Fast-paced, two-player action on a single keyboard.
* **7-Layered Rendering Pipeline:** Features an ultra-dark space void, semi-transparent alpha-blended nebulae (`SRCALPHA`), a 3-layer parallax scrolling starfield, orbiting celestial bodies, hazards, and a real-time HUD display.
* **Dynamic Resource Management:** An ammo economy system where players start with 0 ammunition and must compete for golden Mystery Boxes to reload.
* **Freeze-on-Hit Mechanic:** Getting hit by an enemy laser freezes a ship in pure white for 2000ms, disabling movement and shooting.
* **Black Hole Wave Events:** A timed hazard system that spawns three pulsing black holes with gravitational repulsion logic during the last 10 seconds of every minute.

---

## 🛠️ Tech Stack & Tools

* **Language:** Python 3.x
* **Graphics Engine:** Pygame 2.x
* **Mathematical Operations:** Python `math` module (Trigonometric functions for orbital loops, Euclidean distance for circular collisions).
* **Procedural Logic:** Python `random` module (for unique asteroid vertex positioning, starfield distribution, and spawn quadrants).

---

## 📐 Applied Computer Graphics Concepts

This project implements core engineering and computer graphics standards from scratch:

### 1. 2D Transformations
* **Translation:** Smooth coordinate updates for player ships, lasers, and moving hazards based on velocity vectors.
* **Rotation (Orbital Mechanics):** Planets and moons utilize continuous parametric angle increments calculated via:
    $$x = \text{origin}_x + \cos(\theta) \times \text{distance}$$
    $$y = \text{origin}_y + \sin(\theta) \times \text{distance}$$
* **Scaling & Animation:** Multi-layer star parallax depth scrolling (0.3px to 0.9px per frame), per-star twinkle brightness shifting, and sine-wave driven pulsing animations for Black Holes and Mystery Boxes.

### 2. Collision Detection Systems
* **Circular Distance-Based Collision:** Uses Euclidean distance optimization (`math.hypot`) for player interactions with asteroids, collectibles, and black holes.
* **Axis-Aligned Bounding Box (AABB):** Checks overlap boundaries (left, right, top, bottom) for precise laser-to-player hits.

### 3. Procedural Shape Generation
* Asteroids are generated dynamically using an irregular 8-vertex polygon routine. Vertices are placed at $45^\circ$ intervals with randomized radii ranging between 70% and 130% of the base radius to form uniquely jagged configurations.

---

## 📂 Code Architecture

The repository is built following clean Object-Oriented Programming (OOP) principles and modular decoupling:

```text
├── main.py              # Central game loop, states (Menu, Game, Summary), and HUD logic
├── player.py            # Player class; handles movement input, ammo counts, and freeze states
├── ship.py              # Abstract base class managing base positions, speed, and laser instances
├── laser.py             # Projectile handling, dual-layer rendering (plasma core + neon glow), and AABB
├── celestial.py         # Subclasses for Asteroid, CelestialBody, and MysteryBox geometry
├── celestial_manager.py # HazardManager for centralized spawning, updating, and cleanup
├── level.py             # Renders procedural starfields and translucent nebula clouds
└── sprites.py           # Universal color constants and glowing visual utility functions
