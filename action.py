from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Actor, Entity, Item


class Action:
    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        return self.entity.gamemap.engine

    def perform(self) -> None:
        raise NotImplementedError()


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        return self.engine.game_map.get_blocking_entity(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_loc(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack")

        damage = self.entity.fighter.power - target.fighter.defense
        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_atk
        else:
            attack_color = color.enemy_atk

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} hit points", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage", attack_color
            )


class MovementAction(ActionWithDirection):
    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bound(dest_x, dest_y):
            raise exceptions.Impossible("That way is blocked")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            raise exceptions.Impossible("That way is blocked")
        if self.engine.game_map.get_blocking_entity(dest_x, dest_y):
            raise exceptions.Impossible("That way is blocked")

        self.entity.move(self.dx, self.dy)


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()

        else:
            return MovementAction(self.entity, self.dx, self.dy).perform()


class WaitAction(Action):
    def perform(self) -> None:
        pass


class TakeStairsAction(Action):
    def perform(self) -> None:
        if (self.entity.x, self.entity.y) == self.engine.game_map.downstairs_loc:
            self.engine.message_log.add_message(
                "You descend the staircase", color.descend
            )
            self.engine.game_world.generate_floor()
        else:
            raise exceptions.Impossible("There ar no stairs here")


class ItemAction(Action):
    def __init__(
        self, entity: Actor, Item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = Item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(actor) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_loc(*self.target_xy)

    def perform(self) -> None:
        if self.item.consumable:
            self.item.consumable.activate(self)


class PickupAction(Action):
    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_loc_x = self.entity.x
        actor_loc_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_loc_x == item.x and actor_loc_y == item.y:
                if len(inventory.items) >= inventory.capactiy:
                    raise exceptions.Impossible("Your inventory is full")

                self.engine.game_map.entities.remove(item)
                item.parent = self.entity.inventory
                inventory.items.append(item)

                self.engine.message_log.add_message(f"You picked up {item.name}")
                return
        raise exceptions.Impossible("There is nothing to pick up here")


class DropItem(ItemAction):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity, item)

    def perform(self) -> None:
        if self.entity.equipment.item_is_equipped(self.item):
            self.entity.equipment.toggle_equip(self.item)

        self.entity.inventory.drop(self.item)


class EquipAction(ItemAction):
    def __init__(self, entity: Actor, item: Item):
        super().__init__(entity, item)

    def perform(self) -> None:
        self.entity.equipment.toggle_equip(self.item)
