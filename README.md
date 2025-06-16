# 🎵 Rhythm Dodge
**A dynamic rhythm-based dodge game built with Pygame!**

**Players control a character to dodge obstacles and survive the beat!**

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/cover.png" width="600">

## 🚀 Features

✅ **Dynamic Obstacles — Includes multiple obstacle types:**

⚙️ GearObstacle: Rotating gears with teeth that spin continuously.

🔵 LaserCircleObstacle: Charging laser circles with animated stages (charge, fire, fade).

🎯 CannonObstacle: Cannons that shoot projectiles at adjustable rates and directions.

✅ **Screen Shake Effect —** Built-in shake method for all obstacles, adding impactful camera shake during hits or special events.

✅ **Configurable Intensity —** Customize shake duration and magnitude per obstacle for varied dramatic effects.

✅ **Smooth Animations —** Obstacles update their own rotation, alpha transitions, and expansion over time for a polished visual experience.

✅ **Modular Design —** Clear class hierarchy (CircleObstacle, RectObstacle → specific bosses) for easy extension and reuse.

✅ **Performance Friendly —** Uses lightweight Pygame drawing with alpha blending and efficient update loops.

✅ **Plug-and-Play —** Just create obstacles, call update() and draw(), and trigger shake() whenever needed — no extra setup.

✅ **Future-Proof —** Easy to add more obstacle types, patterns, or AI behaviors thanks to clean OOP structure.

## 📂 Project Structure

```Rhythm Dodge/
Rhythm Dodge/
├── main.py              # Main game loop
├── player.py            # Player class
├── obstacle.py          # Obstacle classes
├── timeline.py          # Timeline and obstacle spawner
├── particle.py          # Particle effects
├── ui.py                # HUD and UI rendering
├── screens/             # Game screen modules
│   ├── start.py         # Start screen
│   ├── tutorial.py      # Tutorial screen     
│   ├── main_menu.py     # Main menu
│   ├── pause.py         # Pause menu
│   ├── win_screen.py    # Victory screen
│   ├── gameover.py      # Game over screen
├── levels/              # Level timeline data
│   ├── level1.json      # Level 1 event timeline
│   ├── level2.json      # Level 2 event timeline
├── assets/              # Game assets
│   ├── music/           # Background music
│   ├── sound_effect/    # Sound effects
│   ├── images/          # Sprites and textures
│   ├── fonts/           # Font files
├── beats_to_json/       # Beat extraction utility
│   ├── beats_to_json    # Convert music beats to JSON
├── README.md            # Project documentation
```

## Class Diagram

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/diagram.png" width="600">

## 🗂️ JSON Level Format
Each level has a .json that defines the sequence of events.

*Example:*

```json
[
  {"time": 1000, "type": "obstacle_type", "params": {...}},
  {"time": 2000, "type": "another_obstacle", "params": {...}}
]
```

## 🎮 How to Play

- **Arrow keys** to move.
- **Dash**: (depends on your `Player` implementation)
- Survive by dodging obstacles in sync with the music.
- Press **ESC** to pause the game.
- Reach the end of the song to win!

### 💡 Steps

1. **Enter the tutorial to learn how to play the game.**

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/tutor.png" width="600">

2. **Select a song to play.**

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/menu.png" width="600">

3. **Use the arrow keys to move the player left and right.**

4. **Dodge the obstacles that spawn at the top of the screen.**

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/play.png" width="600">

5. **Player's blood decreases when the player collides with an obstacle.**

6. **The game ends when the player's blood reaches zero.**

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/over.png" width="600">

## 🏆 To Do / Ideas

✅ Custom levels

✅ Particle effects

✅ Pause & resume

✅ Victory and game over screens

✅ Radial beams visual effect


