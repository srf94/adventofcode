from copy import copy
from utils import read_data
from intcode_vm import run_instructions, intcode_send


def draw_board(tiles):
    tiles = copy.copy(tiles)
    for tile in tiles:
        for loc in range(len(tile)):
            tile[loc] = str(tile[loc]). \
                replace('0', ' '). \
                replace('2', 'B'). \
                replace('3', '_'). \
                replace('4', 'O')

    print("\n".join("".join(str(i) for i in tile) for tile in tiles))


def print_tuple(x, y, tile):
    if tile == 3:
        name = "Paddle"
    elif tile == 4:
        name = "Ball"
    else:
        return
    print("{}: x: {}, y: {}".format(name, x, y))


def single_step(value, gen):
    triple = []
    for i in range(3):
        value = intcode_send(gen, value)
        triple.append(value)
    return tuple(triple)


def get_location(board, last, paddle=False, ball=False):
    if paddle:
        val = 3
    elif ball:
        val = 4
    else:
        raise Exception()
    for y, row in enumerate(board):
        for x, value in enumerate(row):
            if value == val:
                return x, y
    return last


def ball_intersection(paddle_loc, ball_loc, ball_direction):
    return ball_loc[0] + (paddle_loc[1] - ball_loc[1] - 1) * ball_direction


def create_board(generator_input, gen, dim_x, dim_y):
    total_pixels = dim_x * dim_y
    board = [[0] * dim_x for _ in range(dim_y)]

    for _ in xrange(total_pixels):
        x, y, tile = single_step(generator_input, gen)
        board[y][x] = tile
    return board


def play_game(board):
    ball_direction = 1
    ball_loc = None
    paddle_loc = None
    last_score = None
    ball_locs = []

    while True:
        ball_loc = get_location(board, ball_loc, ball=True)
        paddle_loc = get_location(board, paddle_loc, paddle=True)
        ball_locs.append(ball_loc)

        if len(ball_locs) > 1:
            diff = ball_locs[-1][0] - ball_locs[-2][0]
            if diff != 0:
                ball_direction = diff

        intersection = ball_intersection(paddle_loc, ball_loc, ball_direction)

        if intersection > paddle_loc[0]:
            direction = 1
        elif intersection < paddle_loc[0]:
            direction = -1
        else:
            direction = 0

        try:
            x, y, tile = single_step(direction, gen)
        except:
            return last_score

        if x == -1:
            last_score = tile
        else:
            board[y][x] = tile


raw = read_data(13)[0].split(",")
dim_x = 44
dim_y = 20


gen = run_instructions(raw, debug=False)
board = create_board(0, gen, dim_x, dim_y)
print("Part 1:")
print(sum(sum(i == 2 for i in row) for row in board))


raw[0] = 2
gen = run_instructions(raw, debug=False)
board = create_board(0, gen, dim_x, dim_y)


print("Part 2:")
print(play_game(board))
