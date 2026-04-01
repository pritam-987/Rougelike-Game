import traceback

import tcod

import color
import event_handlers
import exceptions
import setup_game
from utils import resource_path


def save_game(handler: event_handlers.BaseEventHandler, filename: str) -> None:
    if isinstance(handler, event_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved")


def main() -> None:
    width = 80
    height = 50

    tileset = tcod.tileset.load_tilesheet(
        resource_path("dejavu10x10_gs_tc.png"), 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    handler: event_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
        width, height, tileset=tileset, title="Rougelike", vsync=True
    ) as context:
        root_console = tcod.Console(width, height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:
                    traceback.print_exc()
                    if hasattr(handler, "engine"):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:
            save_game(handler, "savegame.sav")
            raise
        except BaseException:
            save_game(handler, "savegame.sav")
            raise


if __name__ == "__main__":
    main()
