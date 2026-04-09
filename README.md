

##Declaration 
AI was used to write some parts of the readme.

# Introduction

## What is this?
This is a clone of the original Rogue game which I have made in tcod and python.

## Game Summary
You can play as "@" the player, explore dungeon, level up and have fun.


* `@` Player
* `o` Orc
* `T` Troll
* `!` Potion
* `>` Stairs

---

# Installation

## Requirements

 Python 3.8+
 tcod library

Install dependencies:

```
pip install tcod
```

Clone the repository:

```
git clone https://github.com/pritam-987/rouge.git
cd rouge
```

---

# How to Play

## Getting Started

Run the game:

Dowonload the main.exe file from release page and run the file.

From the main menu:

* Press "N" to start a new game



---

## Combat

Combat is automatic when you move into an enemy.

Enemies attack you during their turn.

Use scrolls and potions strategically to survive.

---

## Leveling Up

Killing enemies grants XP and XP unlocks new levels. You can select powerups after leveling up.

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

## Stairs

```
>
```
Press Shift + . to acess the stairs.gg













