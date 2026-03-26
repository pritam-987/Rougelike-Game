import tcod


def main() -> None:
    width = 80
    height = 50

    player_x = int(width / 2)
    player_y = int(height / 2)

    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    with tcod.context.new_terminal(
        width, height, tileset=tileset, title="Rougelike", vsync=True
    ) as context:
        root_console = tcod.Console(width, height, order="F")
        while True:
            root_console.print(x=player_x, y=player_y, string="@")
            context.present(root_console)

            for event in tcod.event.wait():
                if event.type == "QUIT":
                    raise SystemExit()


if __name__ == "__main__":
    main()
