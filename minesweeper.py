import argparse
from random import randint

MINE = -1
HIDDEN_STATUS = 'hidden'
EXPOSED_STATUS = 'exposed'
HIDDEN_REPR = '-'
MINE_REPR = '@'


def get_cell_neighbors(board: list[list[dict]], x: int, y: int) -> list[tuple[int, int]]:
    return [(x+i, y+j) for i, j
            in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
            if (0 <= (x+i) < len(board)) and (0 <= (y+j) < len(board))]


def cell_to_string(cell: dict) -> str:
    '''stringify cell for printing'''
    if cell['status'] == HIDDEN_STATUS:
        return HIDDEN_REPR
    if cell['value'] == MINE:
        return MINE_REPR
    return str(cell['value'])


def draw_board(board: list[list[dict]]) -> None:
    '''draw the board to the terminal'''
    for row in board:
        for cell in row:
            print(cell_to_string(cell), end=' ')
        print('')


# init the board and positioning mines
def init_board(size: int, num_of_mines: int):
    board = [[{'value': 0,
              'status': HIDDEN_STATUS} for _ in range(size)] for _ in range(size)]
    mines_left = num_of_mines
    while mines_left > 0:
        x, y = randint(0, size-1), randint(0, size-1)
        if board[x][y]['value'] != MINE:
            board[x][y]['value'] = MINE
            mines_left -= 1
            for i, j in get_cell_neighbors(board, x, y):
                if board[i][j]['value'] != MINE:
                    board[i][j]['value'] += 1
    return board


def click(board, x, y) -> int:
    '''recursively exposing cells, if expose empty cell expose all those around it'''
    if board[x][y]['status'] == EXPOSED_STATUS:
        return 0
    board[x][y]['status'] = EXPOSED_STATUS
    if board[x][y]['value'] == MINE:
        return None
    exposed_count = 1
    if board[x][y]['value'] == 0:
        for i, j in get_cell_neighbors(board, x, y):
            exposed_count += click(board, i, j)
    return exposed_count


def first_click(board):
    found = False
    while not found:
        x, y = randint(0, (size := len(board)-1)), randint(0, size)
        found = board[x][y]['value'] == 0
    return click(board, x, y)


def get_user_coord(size: int, text: str) -> int:
    try:
        coord = int(input(text))
        if coord >= size or coord < 0:
            raise Exception()
        return coord
    except Exception as e:
        print(f'coordinate must be a number between 0 and {size - 1}')
        return get_user_coord(size, text)


def run_game(size: int, num_of_mines: int):
    board = init_board(size, num_of_mines)
    exposed_cells = first_click(board)
    draw_board(board)
    while not exposed_cells == (size*size - num_of_mines):
        x, y = get_user_coord(
            size, f'row (0 to {size-1}): '), get_user_coord(size, f'column (0 to {size-1}): ')
        res = click(board, x, y)
        draw_board(board)
        if res == None:
            print('GAME OVER')
            return
        exposed_cells += res
    print('WIN!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='simple minesweeper game')
    parser.add_argument('board_size', type=int,
                        help='size of the board (s*s)')
    parser.add_argument('mines', type=int,
                        help='number of mines')

    args = parser.parse_args()
    run_game(args.board_size, args.mines)
