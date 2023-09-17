import numpy as np
import pygame
from tensorflow import keras

# prepare data model
# 28 * 28 = 784 input nodes
# 784 / 4 = 196 nodes in hidden layer 1
# 784 / 4 = 196 nodes in hidden layer 2
# 10 nodes in output layer (0-9)
model = keras.Sequential(
    [
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(196, activation="linear"),
        keras.layers.Dense(196, activation="linear"),
        keras.layers.Dense(10, activation="softmax"),
    ]
)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

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

DATA_DOWNLOADED = False

TILES = 28
TOP_PADDING = 100
WINDOW_WIDTH, WINDOW_HEIGHT = 700, 700 + TOP_PADDING
TILE_SIZE = WINDOW_WIDTH / TILES
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
BUTTON_POS_X, BUTTON_POS_Y = (
    WINDOW_WIDTH / 2 - BUTTON_WIDTH / 2,
    TOP_PADDING - BUTTON_HEIGHT,
)


board = np.zeros((TILES, TILES), dtype=int)


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

    for row in range(TILES):
        for col in range(TILES):
            if board[row, col]:
                pygame.draw.rect(
                    WIN,
                    COLORS["black"],
                    (
                        col * TILE_SIZE,
                        TOP_PADDING + (row * TILE_SIZE),
                        TILE_SIZE,
                        TILE_SIZE,
                    ),
                )

            else:
                pygame.draw.rect(
                    WIN,
                    COLORS["tile"],
                    (
                        col * TILE_SIZE,
                        TOP_PADDING + (row * TILE_SIZE),
                        TILE_SIZE,
                        TILE_SIZE,
                    ),
                )

    pygame.display.update()


def handleAI():
    global DATA_DOWNLOADED

    if not DATA_DOWNLOADED:
        DATA_DOWNLOADED = True

        # load images to train
        (train_images, train_labels) = keras.datasets.mnist.load_data(path="mnist.npz")[
            0
        ]

        # squash every pixel between 0 and 1
        train_images = train_images / 255.0

        # training the model
        model.fit(train_images, train_labels, epochs=2)

    board_reshaped = np.expand_dims(board, axis=0)
    predictions = model.predict(board_reshaped)
    print(f"{np.argmax(predictions[0])} - {round(max(predictions[0]) * 100, 2)}%")


def checkIfBoardCorrect():
    for row in range(TILES):
        for col in range(TILES):
            if board[row, col]:
                return True
    return False


def clearBoard():
    global board
    board = np.zeros((TILES, TILES), dtype=int)


def handleMouseClick(mousePos, mouseButton):
    mouseX, mouseY = mousePos
    if (
        BUTTON_POS_X <= mouseX <= BUTTON_POS_X + BUTTON_WIDTH
        and BUTTON_POS_Y <= mouseY <= BUTTON_POS_Y + BUTTON_HEIGHT
    ):
        if not checkIfBoardCorrect():
            return

        handleAI()
        clearBoard()
        return

    if mouseY < TOP_PADDING:
        return

    tileX, tileY = int(mouseX / TILE_SIZE), int((mouseY - TOP_PADDING) / TILE_SIZE)
    if TILES >= tileY >= 0 and TILES >= tileX >= 0:
        if mouseButton[0]:
            board[tileY, tileX] = 1
        elif mouseButton[2]:
            board[tileY, tileX] = 0


def main():
    WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("NUMBERS")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                mousePos = pygame.mouse.get_pos()
                handleMouseClick(mousePos, pygame.mouse.get_pressed())

        draw(WIN)


if __name__ == "__main__":
    main()
