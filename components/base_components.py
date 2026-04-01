from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class BaseComponent:
    parent: Entity

    @property
    def gamemap(self) -> None:
        return self.parent.gamemap

    @property
    def engine(self) -> Engine:
        return self.gamemap.engine
