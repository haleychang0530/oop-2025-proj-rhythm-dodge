# 🎵 **Rhythm Dodge**
*A dynamic rhythm-based dodge game built with Pygame!*

Dodge, dash, and survive the beat — challenge your reflexes and groove to the rhythm!

---

## 🚀 **Features**

### ✅ **Dynamic Obstacles**
- ⚙️ **GearObstacle:** Rotating gears with spinning teeth.
- 🔵 **LaserCircleObstacle:** Multi-phase laser rings (charge → fire → fade).
- 🎯 **CannonObstacle:** Cannons that fire projectiles at customizable speeds and angles.

### ✅ **Impactful Screen Shake**
Built-in camera shake for all obstacles — amplify hits and special effects for dramatic flair.

### ✅ **JSON Level Design**
Define obstacle patterns and timings in a simple JSON format for easy level design.
Create the timeline to perform the beats of songs!

### ✅ **Particle Effects**
Create stunning visual feedback with particles that follow the player, enhancing immersion.

### ✅ **Customizable Intensity**
Adjust shake duration and magnitude per obstacle to create unique tension and vibe.

### ✅ **Smooth Animations**
Polished obstacle rotation, transparency, and scale transitions for fluid visual feedback.

### ✅ **Performance Optimized**
Lightweight Pygame drawing, alpha blending, and efficient update loops.

### ✅ **Plug-and-Play**
Create obstacles, call `update()` and `draw()`, trigger `shake()` as needed — minimal setup!

### ✅ **Future-Proof**
Seamlessly expand with new obstacles, patterns, AI, or levels — all thanks to clean OOP architecture.

---

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
### ✅ **OOP and Class Diagram**
Clear class hierarchy:

Easy to extend and reuse for new obstacle types or game modes.

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/diagram.jpg" width="800">

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

`Screen: Start Interface`

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/cover.png" width="800">

***

#### 1️⃣ **Enter the tutorial to learn how to play the game.**

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/tutor.png" width="800">

***

#### 2️⃣ **Select a song to play.**

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/menu.png" width="800">

***

#### 3️⃣ **Use the arrow keys to move the player left and right.**

```
Example : Particle effect. Move right and particles will follow!

Obstacles shake the screen when the player is hit.

```

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/particle.jpg" width="800">

***

#### 4️⃣ **Dodge the obstacles that spawn at the top of the screen.**

`Example : Gear obstacle. Dodge it!`

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/play_bomb.png" width="800">

`Example : Ring obstacle. Dash to penetrate!`

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/play_ring.png" width="800">

***

#### 5️⃣ **Player's blood decreases when the player collides with an obstacle.**

***

#### 6️⃣ **The game ends when the player's blood reaches zero.**

`Screen: Game over screen. Try again or quit!`

<img src="https://github.com/haleychang0530/oop-2025-proj-rhythm-dodge/blob/main/assets/images/over.png" width="800">



## 🏆 To Do / Ideas

✅ Custom levels

✅ Particle effects

✅ Pause & resume

✅ Victory and game over screens

✅ Radial beams visual effect


