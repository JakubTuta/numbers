import os

import numpy as np
import pygame
from tensorflow import keras

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

model = None
LAST_NUMBER = ""
PREDICTION = ""

board = np.zeros((TILES, TILES), dtype=int)


def draw_button(WIN):
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


def draw_text(WIN):
    text = "Draw the number:"
    textLabel = font.render(f"{text}", True, COLORS["black"])
    textWidth = font.size(f"{text}")[0]

    WIN.blit(textLabel, (WINDOW_WIDTH / 2 - textWidth / 2, 10))

    lastNumberLabel = font2.render(f"Last number: {LAST_NUMBER}", True, COLORS["black"])
    WIN.blit(lastNumberLabel, (10, 10))

    predictionLabel = font2.render(f"Prediction: {PREDICTION}%", True, COLORS["black"])
    WIN.blit(predictionLabel, (10, 50))


def draw_board(WIN):
    for row in range(TILES):
        for col in range(TILES):
            if board[row, col]:
                color = "black"
            else:
                color = "tile"

            pygame.draw.rect(
                surface=WIN,
                color=COLORS[color],
                rect=(
                    col * TILE_SIZE,
                    TOP_PADDING + (row * TILE_SIZE),
                    TILE_SIZE,
                    TILE_SIZE,
                ),
            )


def draw(WIN):
    WIN.fill(COLORS["background"])

    draw_button(WIN)
    draw_text(WIN)
    draw_board(WIN)

    pygame.display.update()


def handleAI():
    global LAST_NUMBER
    global PREDICTION

    board_reshaped = np.expand_dims(board, axis=0)
    predictions = model.predict(board_reshaped)

    LAST_NUMBER = np.argmax(predictions[0])
    PREDICTION = round(max(predictions[0]) * 100, 2)


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


def folderExists():
    folder_name = "handwritten.model"
    folder_path = os.path.join("./", folder_name)

    return os.path.exists(folder_path) and os.path.isdir(folder_path)


def prepareAI():
    global model

    if not folderExists():
        # load images to train
        (train_images, train_labels) = keras.datasets.mnist.load_data(path="mnist.npz")[
            0
        ]

        # squash every pixel between 0 and 1
        train_images = keras.utils.normalize(train_images, axis=1)

        # prepare data model
        # 28 * 28 = 784 input nodes
        # 128 nodes in hidden layer 1
        # 128 nodes in hidden layer 2
        # 10 nodes in output layer (0-9)
        model = keras.Sequential(
            [
                keras.layers.Flatten(input_shape=(TILES, TILES)),
                keras.layers.Dense(128, activation="relu"),
                keras.layers.Dense(128, activation="relu"),
                keras.layers.Dense(10, activation="softmax"),
            ]
        )

        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

        model.fit(train_images, train_labels, epochs=3)

        model.save("handwritten.model")

    else:
        model = keras.models.load_model("handwritten.model")


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
    prepareAI()
    main()
