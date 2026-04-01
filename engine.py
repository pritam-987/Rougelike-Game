from __future__ import annotations

import lzma
import pickle
from typing import TYPE_CHECKING, Any, Iterable

from tcod.console import Console
from tcod.map import compute_fov

import exceptions
import render_functions
from message_log import MessageLog

if TYPE_CHECKING:
    from entity import Actor
    from event_handlers import EventHandler
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    event_handler: EventHandler
    game_world: GameWorld

    def __init__(
        self,
        player: Actor,
        game_map: GameMap = None,
        event_handler: EventHandler = None,
    ):
        self.player = player
        self.game_map = game_map
        self.mouse_loc = (0, 0)
        self.message_log = MessageLog()

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            action.perform(self, self.player)
            self.handle_enemy_turns()

            self.update_fov()

    def render(
        self,
        console: Console,
    ) -> None:
        self.game_map.render(console)
        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            max_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            loc=(0, 47),
        )

        render_functions.render_names_at_loc(console=console, x=21, y=44, engine=self)

    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"], (self.player.x, self.player.y), radius=8
        )
        self.game_map.explored |= self.game_map.visible

    def save_as(self, filename: str) -> None:
        save_data = lzma.compress(pickle.dumps(self))
        with open(filename, "wb") as f:
            f.write(save_data)
