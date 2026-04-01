from __future__ import annotations

from typing import TYPE_CHECKING, Tuple

import color

if TYPE_CHECKING:
    from tcod import Console

    from game_map import GameMap


def get_names_at_loc(x: int, y: int, game_map: GameMap) -> str:
    if not game_map.in_bound(x, y) or not game_map.visible[int(x), int(y)]:
        return ""

    names = ", ".join(
        entity.name for entity in game_map.entities if entity.x == x and entity.y == y
    )

    return names.capitalize()


def render_bar(
    console: Console, current_value: int, max_value: int, total_width: int
) -> None:
    bar_width = int(float(current_value) / max_value * total_width)

    console.draw_rect(x=0, y=45, width=total_width, height=1, ch=1, bg=color.bar_empty)

    if bar_width > 0:
        console.draw_rect(
            x=0, y=45, width=bar_width, height=1, ch=1, bg=color.bar_filled
        )

    console.print(
        x=1, y=45, string=f"HP: {current_value}/{max_value}", fg=color.bar_text
    )


def render_dungeon_level(
    console: Console, dungeon_level: int, loc: Tuple[int, int]
) -> None:
    x, y = loc
    console.print(x=x, y=y, string=f"Dungeon level: {dungeon_level}")


def render_names_at_loc(console: Console, x: int, y: int, engine: Engine) -> None:
    mouse_x, mouse_y = engine.mouse_loc

    names_at_loc = get_names_at_loc(x=mouse_x, y=mouse_y, game_map=engine.game_map)
    console.print(x=x, y=y, string=names_at_loc)
