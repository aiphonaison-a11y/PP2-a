# 🐍 Snake Game with Levels, Food & Poison

## 📌 Overview

This project is a classic Snake game built using **Pygame**, enhanced with additional gameplay mechanics such as scoring, random poison, and a game over system.

The player controls a snake that grows by eating food and must avoid collisions with itself and the game boundaries. Occasionally, poison appears, introducing risk and strategy.

---

## 🎮 Features

* ✅ Smooth snake movement with keyboard controls
* 🍎 **Food system** (red blocks)

  * Increases snake length
  * Increases score
* ☠️ **Poison system** (vivid violet blocks)

  * Appears randomly
  * Disappears after a short time
  * Decreases snake length and score
* 📊 **Score tracking** displayed in real time
* 💀 **Game Over screen**

  * Displays final score
  * Restart (R) or Quit (Q) options
* 🔁 Continuous gameplay loop

---

## 🕹️ Controls

| Key | Action                  |
| --- | ----------------------- |
| ↑   | Move Up                 |
| ↓   | Move Down               |
| ←   | Move Left               |
| →   | Move Right              |
| R   | Restart after Game Over |
| Q   | Quit game               |

---

## ⚙️ Requirements

* Python 3.x
* Pygame

Install Pygame using:

```bash
pip install pygame
```

---

## ▶️ How to Run

1. Make sure both files are in the same folder:

   * `main.py`
   * `snake.py`

2. Run the game:

```bash
python main.py
```

---

## 🧠 Game Logic

* The snake moves in a grid-based system.
* Eating food:

  * Snake grows by 1 segment
  * Score increases
* Eating poison:

  * Snake shrinks
  * Score decreases (not below 0)
* Game ends if:

  * Snake hits the wall
  * Snake collides with itself

---

## 🎯 Objective

Survive as long as possible and achieve the highest score by balancing risk (poison) and reward (food).

---

## 📷 Visual Design

* **Red** → Food (safe, beneficial)
* **Violet** → Poison (dangerous, temporary)
* **White/Grey** → Snake body

---

## 🚀 Possible Improvements

* Add sound effects or background music
* Increase speed with score
* Add obstacles or levels
* Save high scores
* Add animations

---

## 👩‍💻 Author

Created as part of a Python/Pygame learning project.

---

## 📄 License

This project is for educational purposes.
