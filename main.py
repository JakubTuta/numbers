import pygame

pygame.init()
font = pygame.font.SysFont(None, 50)
font2 = pygame.font.SysFont(None, 30)

COLORS = {
    "background": (100, 100, 100),
    "tile": (200, 200, 200),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "gray": (127, 127, 127),
}

TILES = 28
TOP_PADDING = 100
WINDOW_WIDTH, WINDOW_HEIGHT = 700, 700 + TOP_PADDING
TILE_SIZE = WINDOW_WIDTH / TILES
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
BUTTON_POS_X, BUTTON_POS_Y = (
    WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2,
    TOP_PADDING - BUTTON_HEIGHT,
)


board = [[" " for _ in range(28)] for __ in range(28)]


def draw(WIN):
    WIN.fill(COLORS["background"])

    text = "Draw the number:"
    textLabel = font.render(f"{text}", True, COLORS["black"])
    textWidth, textHeight = font.size(f"{text}")

    WIN.blit(textLabel, (WINDOW_WIDTH / 2 - textWidth / 2, 10))

    pygame.draw.rect(
        WIN,
        COLORS["gray"],
        (
            BUTTON_POS_X,
            BUTTON_POS_Y,
            BUTTON_WIDTH,
            BUTTON_HEIGHT,
        ),
    )

    text2 = "Send"
    sendLabel = font2.render(f"{text2}", True, COLORS["white"])
    textWidth2, textHeight2 = font2.size(f"{text2}")

    WIN.blit(
        sendLabel,
        (
            WINDOW_WIDTH / 2 - textWidth2 / 2,
            BUTTON_POS_Y + BUTTON_HEIGHT / 2 - textHeight2 / 2,
        ),
    )

    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if col == " ":
                pygame.draw.rect(
                    WIN,
                    COLORS["tile"],
                    (
                        x * TILE_SIZE,
                        TOP_PADDING + (y * TILE_SIZE),
                        TILE_SIZE,
                        TILE_SIZE,
                    ),
                )

            elif col == "*":
                pygame.draw.rect(
                    WIN,
                    COLORS["black"],
                    (
                        x * TILE_SIZE,
                        TOP_PADDING + (y * TILE_SIZE),
                        TILE_SIZE,
                        TILE_SIZE,
                    ),
                )

    pygame.display.update()


def handleMouseClick(mousePos):
    mouseX, mouseY = mousePos
    if (
        BUTTON_POS_X <= mouseX <= BUTTON_POS_X + BUTTON_WIDTH
        and BUTTON_POS_Y <= mouseY <= BUTTON_POS_Y + BUTTON_HEIGHT
    ):
        print("send to bot")
        return

    tileX, tileY = int(mouseX / TILE_SIZE), int((mouseY - TOP_PADDING) / TILE_SIZE)
    if TILES >= tileY >= 0 and TILES >= tileX >= 0 and board[tileY][tileX] == " ":
        board[tileY][tileX] = "*"


def main():
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("NUMBERS")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if pygame.mouse.get_pressed()[0]:
                mousePos = pygame.mouse.get_pos()
                handleMouseClick(mousePos)

        draw(WIN)


if __name__ == "__main__":
    main()
