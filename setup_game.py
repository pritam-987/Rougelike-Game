from __future__ import annotations

import copy
import lzma
import pickle
import traceback
from typing import Optional

import tcod

import color
import entity_factories
import event_handlers
from engine import Engine
from game_map import GameWorld
from utils import resource_path

bg_img = tcod.image.load(resource_path("menu_background(1).png"))[:, :, :3]


def new_game() -> Engine:
    map_width = 80
    map_height = 43

    max_room_size = 10
    min_room_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player)
    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        min_room_size=min_room_size,
        max_room_size=max_room_size,
        map_width=map_width,
        map_height=map_height,
    )
    engine.game_world.generate_floor()
    engine.update_fov()
    engine.message_log.add_message(
        "Hello and welcome, adventurer, to the dungeon!", color.welcome_text
    )
    dagger = copy.deepcopy(entity_factories.dagger)
    leather_armor = copy.deepcopy(entity_factories.leather_armor)

    dagger.parent = player.inventory
    leather_armor.parent = player.inventory

    player.inventory.items.append(dagger)
    player.equipment.toggle_equip(dagger, add_message=False)

    player.inventory.items.append(leather_armor)
    player.equipment.toggle_equip(leather_armor, add_message=False)
    return engine


class MainMenu(event_handlers.BaseEventHandler):
    def on_render(self, console: tcod.Console) -> None:
        console.draw_semigraphics(bg_img, 0, 0)

        console.print(
            console.width // 2,
            console.height // 2 - 4,
            "PyRouge",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )
        console.print(
            console.width // 2,
            console.height - 2,
            "By Pr1tam",
            fg=color.menu_title,
            alignment=tcod.CENTER,
        )

        menu_width = 24
        menu_options = ["[N] Play a new game", "[C] Continue last game", "[Q] Quit"]
        for i, text in enumerate(menu_options):
            console.print(
                console.width // 2,
                console.height - 2 - i,
                text.ljust(menu_width),
                fg=color.menu_text,
                bg=color.black,
                alignment=tcod.CENTER,
                bg_blend=tcod.BKGND_ALPHA(64),
            )

    def ev_keydown(
        self, event: tcod.event.KeyDown
    ) -> Optional[event_handlers.BaseEventHandler]:
        if event.sym in (tcod.event.K_q, tcod.event.K_ESCAPE):
            raise SystemExit()
        elif event.sym == tcod.event.K_c:
            try:
                return event_handlers.MainGameEventHandler(load_game("savegame.sav"))
            except FileNotFoundError:
                return event_handlers.PopupMessage(self, "No saved game to load")
            except Exception as exc:
                traceback.print_exc()
                return event_handlers.PopupMessage(
                    self, f"Failed to load save :\n{exc}"
                )
        elif event.sym == tcod.event.K_n:
            return event_handlers.MainGameEventHandler(new_game())


def load_game(filename: str) -> Engine:
    with open(filename, "rb") as f:
        engine = pickle.loads(lzma.decompress(f.read()))
    assert isinstance(engine, Engine)
    return engine
