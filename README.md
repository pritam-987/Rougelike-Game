# 🗡️ Rouge

```
██████╗  ██████╗ ██╗   ██╗ ██████╗ ███████╗
██╔══██╗██╔═══██╗██║   ██║██╔════╝ ██╔════╝
██████╔╝██║   ██║██║   ██║██║  ███╗█████╗  
██╔══██╗██║   ██║██║   ██║██║   ██║██╔══╝  
██║  ██║╚██████╔╝╚██████╔╝╚██████╔╝███████╗
╚═╝  ╚═╝ ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝
```

# 📜 Introduction

## What is Rouge?

**Rouge** is a classic **roguelike dungeon crawler** built with **Python** using the **tcod library**.
The game features procedural dungeon generation, turn-based combat, enemies, equipment, leveling mechanics, and a traditional ASCII interface inspired by classic roguelikes like **Rogue**, **NetHack**, and **Dungeon Crawl Stone Soup**.

## Game Summary

Explore procedurally generated dungeon floors filled with monsters and items.
Fight enemies, collect equipment, level up your character, and descend deeper into the dungeon.

The game follows traditional roguelike mechanics:

* Turn-based gameplay
* ASCII graphics
* Tactical combat
* Procedurally generated dungeons
* Resource management

## Screenshot

*(Add a screenshot here)*

Example gameplay style:

```
####################
#........o.........#
#......@...........#
#..............T...#
#..........!.......#
#..............>...#
####################
```

* `@` Player
* `o` Orc
* `T` Troll
* `!` Potion
* `>` Stairs

---

# ✨ Features

* Procedural dungeon generation with **rooms and corridors**
* **Turn-based gameplay**
* Multiple enemy types:

  * Orc
  * Troll
* **Item system**

  * Consumables
  * Equipment
* **Equipment system**

  * Weapons
  * Armor
* **Level up system**

  * Increase HP
  * Increase Attack
  * Increase Defense
* **Multiple dungeon floors**
* **Message log** system for game feedback
* **Field of View (FOV)** system
* Classic **ASCII roguelike interface**

---

# 🎮 Controls

## Movement

| Key           | Action                         |
| ------------- | ------------------------------ |
| Arrow Keys    | Move in 4 directions           |
| Numpad 1-9    | Move including diagonals       |
| h, j, k, l    | Vi keys: Left, Down, Up, Right |
| y, u, b, n    | Vi diagonal movement           |
| . or Numpad 5 | Wait (skip turn)               |

---

## Items

| Key | Action                     |
| --- | -------------------------- |
| G   | Pick up item at location   |
| I   | Open inventory (use item)  |
| D   | Open inventory (drop item) |

---

## Other

| Key           | Action               |
| ------------- | -------------------- |
| V             | View message history |
| > (Shift + .) | Descend stairs       |
| Esc           | Quit game            |

---

# ⚙️ Installation

## Requirements

* **Python 3.8+**
* **tcod library**

Install dependencies:

```
pip install tcod
```

Clone the repository:

```
git clone https://github.com/yourusername/rouge.git
cd rouge
```

---

# ▶️ How to Play

## Getting Started

Run the game:

Dowonload the main.exe file from release page and run the file.

From the main menu:

* Press **N** to start a new game

---

## Gameplay Loop

1. Move around the dungeon
2. Fight enemies by bumping into them
3. Pick up items using **G**
4. Use potions and scrolls with **I**
5. Equip weapons and armor
6. Kill enemies to gain XP
7. Level up to increase stats
8. Find stairs **(>)** to go deeper

---

## Combat

Combat is automatic when you move into an enemy.

```
Player Attack = base_power + equipment bonuses
Damage = attack - enemy defense
```

Enemies attack you during their turn.

Use **scrolls and potions** strategically to survive.

---

## Leveling Up

Killing enemies grants **XP**.

XP required:

```
XP Needed = level × 150 + level_up_base
```

Where:

```
level_up_base = 200
```

When leveling up, choose one:

| Option       | Effect     |
| ------------ | ---------- |
| Constitution | +20 HP     |
| Strength     | +1 Attack  |
| Agility      | +1 Defense |

---

# 📁 Project Structure

```
rouge/
├── main.py              # Entry point, game loop, save/load
├── engine.py            # Core game engine class
├── event_handlers.py    # Input handling and UI
├── action.py            # Player actions (move, attack, etc.)
├── entity_factories.py  # Predefined actors and items
├── setup_game.py        # New game setup and menu
├── procgen.py           # Dungeon generation
├── game_map.py          # GameMap and GameWorld classes
├── entity.py            # Entity, Actor, Item classes
├── color.py             # Color definitions
├── tile_types.py        # Tile definitions
├── equipment_types.py   # Equipment slot enum
├── equippable.py        # Equippable item logic
├── exceptions.py        # Custom exceptions
├── message_log.py       # Message logging system
├── render_functions.py  # Rendering helpers
├── render_order.py      # Rendering order enum
├── utils.py             # Utility functions
│
├── components/
│   ├── ai.py            # Enemy AI
│   ├── equipment.py     # Equipment management
│   ├── fighter.py       # HP / attack / defense
│   ├── inventory.py     # Player inventory
│   ├── level.py         # XP and leveling system
│   ├── consumable.py    # Usable items
│   └── base_components.py
```

---

# 🧠 Game Mechanics

## Entities

| Entity | Symbol | HP | Power | Defense | XP |
| ------ | ------ | -- | ----- | ------- | -- |
| Player | @      | 30 | 5     | 2       | —  |
| Orc    | o      | 10 | 3     | 0       | 25 |
| Troll  | T      | 16 | 4     | 1       | 50 |

---

## Items

| Item             | Symbol | Effect                      |
| ---------------- | ------ | --------------------------- |
| Health Potion    | !      | Heal 4 HP                   |
| Lightning Scroll | ~      | 20 damage to nearest enemy  |
| Confusion Scroll | ~      | Confuses enemy for 10 turns |
| Fireball Scroll  | ~      | 12 damage in 3-tile radius  |
| Dagger           | /      | +2 power                    |
| Sword            | /      | +4 power                    |
| Leather Armor    | [      | +1 defense                  |
| Chain Mail       | [      | +3 defense                  |

---

## Stairs

```
>
```

* Located in the **last generated room**
* Press **Shift + .** to descend
* Generates a **new dungeon floor**
* Enemies and items respawn

---

# ⚙️ Configuration

Game parameters:

| Setting               | Value   |
| --------------------- | ------- |
| Map Size              | 80 × 43 |
| Max Rooms             | 30      |
| Room Size             | 6 – 10  |
| Max Monsters per Room | 2       |
| Max Items per Room    | 2       |

---

# 📜 License

This project is licensed under the **MIT License**.

You are free to:

* Use
* Modify
* Distribute

---

# 🙏 Acknowledgements

This project is inspired by the official **tcod roguelike tutorial** and classic roguelike games.

* Rogue
* NetHack
* Dungeon Crawl Stone Soup

---

⭐ If you like this project, consider giving it a star!
