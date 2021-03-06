import tkinter


# ---------------------- #
# -- SIZE OF THE GRID -- #
# ---------------------- #

GRID_SIZE = None

while GRID_SIZE is None:
    GRID_SIZE = input("Size of the grid (min 3 , max = 20): ")

    if not GRID_SIZE.isdigit():
        GRID_SIZE = None

    else:
        GRID_SIZE = int(GRID_SIZE)

        if not 3 <= GRID_SIZE <= 20:
            GRID_SIZE = None


# --------------- #
# -- CONSTANTS -- #
# --------------- #

CROSS, EMPTY, DISK = range(-1, 2)

PLAYERS       = [CROSS, DISK]
ACTUAL_PLAYER = 0

GRID = None


# --------------- #
# -- FOR TESTS -- #
# --------------- #

COORDS_TO_TEST = []

for row in range(GRID_SIZE):
    COORDS_TO_TEST.append([
        (row, col)
        for col in range(GRID_SIZE)
    ])

    COORDS_TO_TEST.append([
        (col, row)
        for col in range(GRID_SIZE)
    ])

COORDS_TO_TEST.append([
    (row, row)
    for row in range(GRID_SIZE)
])

COORDS_TO_TEST.append([
    (GRID_SIZE - row - 1, row)
    for row in range(GRID_SIZE)
])


# ----------------------- #
# -- STATE OF THE GAME -- #
# ----------------------- #

def nextplayer():
    global ACTUAL_PLAYER

    ACTUAL_PLAYER += 1
    ACTUAL_PLAYER %= 2


def reset_game():
    global ACTUAL_PLAYER, GRID, EMPTY

    ACTUAL_PLAYER = 0

    GRID = {
        (row, col): EMPTY
        for row in range(GRID_SIZE)
        for col in range(GRID_SIZE)
    }


def cell_can_be_played(row, col):
    global GRID, EMPTY

    return GRID[row, col] == EMPTY


def addtoken(row, col, token):
    global GRID

    GRID[row, col] = token


def game_state():
# True : someone wins.
# None : noone wins.
# False: next player can play.
    global GRID, GRID_SIZE, EMPTY, COORDS_TO_TEST

# A winner ?
    for onetest in COORDS_TO_TEST:
        total = sum([
            GRID[row, col]
            for (row, col) in onetest
        ])

        if abs(total) == GRID_SIZE:
            return True

# Remaining choices
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if GRID[row, col] == EMPTY:
                return False

# No more choice
    return None


# --------------------------- #
# -- CONSTANTS FOR THE GUI -- #
# --------------------------- #

SYMBOLS = {
    CROSS: "×",
    DISK : "o"
}

WHITE, BLACK = "white", "black"


MAIN_WINDOW = tkinter.Tk()

larg_ecran = MAIN_WINDOW.winfo_screenwidth()
haut_ecran = MAIN_WINDOW.winfo_screenheight()

xydim_fen = int(min(larg_ecran, haut_ecran) * .75)

xpos_fen = larg_ecran//2 - xydim_fen//2
ypos_fen = haut_ecran//2 - xydim_fen//2

MAIN_WINDOW.geometry(
    "{0}x{1}+{2}+{3}".format(
        xydim_fen, xydim_fen,
        xpos_fen, ypos_fen
    )
)


FRAME = tkinter.Frame(master = MAIN_WINDOW)

FRAME.grid(row = 0, column = 0)


XYDIM_CANVAS  = int(xydim_fen * .9)
XYDIM_CANVAS -= XYDIM_CANVAS % 3

CANVAS = tkinter.Canvas(
    master     = FRAME,
    width      = XYDIM_CANVAS - 1,
    height     = XYDIM_CANVAS - 1,
    background = WHITE
)

padforstarting = (xydim_fen - XYDIM_CANVAS) // 2

CANVAS.grid(
    row = 0, column = 0,
    padx = padforstarting,
    pady = padforstarting
)

# Draw the grid once upon the time.
WIDTH_CELL = XYDIM_CANVAS // GRID_SIZE

SHIFT_XY = 5
DIAMETER = WIDTH_CELL - 2*SHIFT_XY

position   = 1 - WIDTH_CELL

for i in range(1, GRID_SIZE + 1):
    position += WIDTH_CELL

    CANVAS.create_line(
        position, 0,
        position, XYDIM_CANVAS,
        width = 2,
        fill  = BLACK
    )

    CANVAS.create_line(
        0, position,
        XYDIM_CANVAS, position,
        width = 2,
        fill  = BLACK
    )


# --------- #
# -- GUI -- #
# --------- #

def drawtoken(row, col, token):
    global CROSS, DISK, \
           CANVAS, WIDTH_CELL, SHIFT_XY, DIAMETER, BLACK

    x_left_up = col*WIDTH_CELL + SHIFT_XY
    y_left_up = row*WIDTH_CELL + SHIFT_XY

    x_right_down = x_left_up + DIAMETER
    y_right_down = y_left_up + DIAMETER

    if token == DISK:
        CANVAS.create_oval(
            x_left_up, y_left_up,
            x_right_down, y_right_down,
            outline = BLACK
        )

    else:
        CANVAS.create_line(
            x_left_up, y_left_up,
            x_right_down, y_right_down,
            width = 2,
            fill  = BLACK
        )

        CANVAS.create_line(
            x_left_up, y_right_down,
            x_right_down, y_left_up,
            width = 2,
            fill  = BLACK
        )


def leftclick(event):
    global PLAYERS, ACTUAL_PLAYER, \
           MAIN_WINDOW, WIDTH_CELL, SYMBOLS

    row = event.y // WIDTH_CELL
    col = event.x // WIDTH_CELL

    if cell_can_be_played(row, col):
        addtoken(row, col, PLAYERS[ACTUAL_PLAYER])
        drawtoken(row, col, PLAYERS[ACTUAL_PLAYER])

        endofgame = game_state()

        if endofgame is None:
            endofgame = True
            title = "No one wins..."

        elif endofgame:
            title = "PLAYER " + str(ACTUAL_PLAYER + 1) + " playing with " \
                  + SYMBOLS[PLAYERS[ACTUAL_PLAYER]] + " has won."

        if endofgame:
            MAIN_WINDOW.title(title + " [SEE YOUR TERMINAL]")

            input("Press some key in the terminal...")
            exit()

        nextplayer()

        MAIN_WINDOW.title(
            'TIC TAC TOE - Player ' + str(ACTUAL_PLAYER + 1) + " plays with " + SYMBOLS[PLAYERS[ACTUAL_PLAYER]]
        )


CANVAS.bind(
    sequence = '<Button-1>',
    func     = leftclick
)


def main():
    global PLAYERS, ACTUAL_PLAYER, \
           MAIN_WINDOW, SYMBOLS

    reset_game()

    MAIN_WINDOW.title(
        'TIC TAC TOE - Player ' + str(ACTUAL_PLAYER + 1) + " plays with " + SYMBOLS[PLAYERS[ACTUAL_PLAYER]]
    )

    MAIN_WINDOW.mainloop()


# ------------------- #
# -- LET'S PLAY... -- #
# ------------------- #

main()
