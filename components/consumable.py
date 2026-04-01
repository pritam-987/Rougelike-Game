from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import action
import color
import components.ai
import components.inventory
from components.base_components import BaseComponent
from event_handlers import (
    ActionOrHandler,
    AreaRangedAttackHAndler,
    SingleRangedAttackHandler,
)
from exceptions import Impossible

if TYPE_CHECKING:
    from entity import Actor, Item


class Consumable(BaseComponent):
    parent: Item

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        return action.ItemAction(consumer, self.parent)

    def activate(self, action: action.ItemAction) -> None:
        raise NotImplementedError()

    def consume(self) -> None:
        entity = self.parent
        inventory = entity.parent
        if isinstance(inventory, components.inventory.Inventory):
            inventory.items.remove(entity)


class HealingConsumable(Consumable):
    def __init__(self, amount: int):
        self.amount = amount

    def activate(self, action: action.ItemAction) -> None:
        consumer = action.entity
        amount_recoverd = consumer.fighter.heal(self.amount)

        if amount_recoverd > 0:
            self.engine.message_log.add_message(
                f"You consume the {self.parent.name}, and recover {amount_recoverd} HP!",
                color.health_recovered,
            )
            self.consume()
        else:
            raise Impossible("Your health is already full")


class LightningDamageConsumable(Consumable):
    def __init__(self, damage: int, max_range: int):
        self.damage = damage
        self.max_range = max_range

    def activate(self, action: action.ItemAction) -> None:
        consumer = action.entity
        target = None
        closest_distance = self.max_range + 1.0

        for actor in self.engine.game_map.actors:
            if actor is not consumer and self.parent.gamemap.visible[actor.x, actor.y]:
                distance = consumer.distance(actor.x, actor.y)

                if distance < closest_distance:
                    target = actor
                    closest_distance = distance

        if target:
            self.engine.message_log.add_message(
                f"A lightning bolt strikes the {target.name} with a loud thunder, for {self.damage}"
            )
            target.fighter.take_damage(self.damage)
            self.consume()
        else:
            raise Impossible("No enemy is close enough to strike")


class ConfusionConsumable(Consumable):
    def __init__(self, num_of_turns: int):
        self.num_of_turns = num_of_turns

    def get_action(self, consumer: Actor) -> Optional[ActionOrHandler]:
        self.engine.message_log.add_message(
            "Select a target location", color.needs_target
        )
        return SingleRangedAttackHandler(
            self.engine,
            callback=lambda xy: action.ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action: action.ItemAction) -> None:
        consumer = action.entity
        target = action.target_actor

        if not self.engine.game_map.visible[action.target_xy]:
            raise Impossible("You can't target an area yo can't see")
        if not target:
            raise Impossible("You must select an enemy to target")
        if target is consumer:
            raise Impossible("You can't confuse yourself")

        self.engine.message_log.add_message(
            f"The eyes of the {target.name} look vacant, as it starts to stumble around!",
            color.status_effect_applied,
        )
        target.ai = components.ai.ConfusedEnemy(
            entity=target,
            previous_ai=target.ai,
            turns_remaining=self.num_of_turns,
        )
        self.consume()


class FireBallDamageConsumable(Consumable):
    def __init__(self, damage: int, radius: int):
        self.damage = damage
        self.radius = radius

    def get_action(self, consumer: Actor) -> AreaRangedAttackHAndler:
        self.engine.message_log.add_message(
            "Select a target location", color.needs_target
        )
        return AreaRangedAttackHAndler(
            self.engine,
            radius=self.radius,
            callback=lambda xy: action.ItemAction(consumer, self.parent, xy),
        )

    def activate(self, action: action.ItemAction) -> None:
        target_xy = action.target_xy
        if not self.engine.game_map.visible[target_xy]:
            raise Impossible("You can't target an area that you can't see")

        target_hit = False
        for actor in self.engine.game_map.actors:
            if actor.distance(*target_xy) == self.radius:
                self.engine.message_log.add_message(
                    f"the {actor.name} is engulfed in a fiery explosion, taking {self.damage} damage"
                )
                actor.fighter.take_damage(self.damage)
                target_hit = True

        if not target_hit:
            raise Impossible("There are no targets in the radius")
        self.consume()
