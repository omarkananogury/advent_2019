text = """
###.#
..#..
#..#.
#....
.#.#.
""".strip()


import numpy as np
from collections import defaultdict


# 1
def adjacent_positions(i, j):
    positions = []
    if i > 0:
        positions.append((i-1, j))
    if i < 4:
        positions.append((i+1, j))
    if j > 0:
        positions.append((i, j-1))
    if j < 4:
        positions.append((i, j+1))
    return positions


def get_dying(board):
    dying = ([], [])
    for i1, j1 in zip(*np.where(board == '#')):
        n_adj_bugs = 0
        for i2, j2 in adjacent_positions(i1, j1):
            if board[i2, j2] == '#':
                n_adj_bugs += 1
        if n_adj_bugs != 1:
            dying[0].append(i1)
            dying[1].append(j1)
    return dying


def get_infesting(board):
    infesting = ([], [])
    for i1, j1 in zip(*np.where(board == '.')):
        n_adj_bugs = 0
        for i2, j2 in adjacent_positions(i1, j1):
            if board[i2, j2] == '#':
                n_adj_bugs += 1
        if n_adj_bugs in {1, 2}:
            infesting[0].append(i1)
            infesting[1].append(j1)
    return infesting


board = np.array([list(x) for x in text.splitlines()])
seen_boards = set()
while True:
    dying, infesting = get_dying(board), get_infesting(board)
    board[dying] = '.'
    board[infesting] = '#'
    board_hash = board.tostring()
    if board_hash in seen_boards:
        break
    seen_boards.add(board_hash)
print(np.power(2, np.where(board.ravel() == '#')[0]).sum())


# 2
def recursive_adjacent_positions(depth, i, j):
    positions = []
    for pos in adjacent_positions(i, j):
        if pos != (2, 2):
            positions.append((depth,) + pos)
    if i == 0:
        positions.append((depth-1, 1, 2))
    elif i == 4:
        positions.append((depth-1, 3, 2))
    if j == 0:
        positions.append((depth-1, 2, 1))
    elif j == 4:
        positions.append((depth-1, 2, 3))
    if (i, j) == (1, 2):
        positions.extend((depth+1, 0, k) for k in range(5))
    elif (i, j) == (3, 2):
        positions.extend((depth+1, 4, k) for k in range(5))
    elif (i, j) == (2, 1):
        positions.extend((depth+1, k, 0) for k in range(5))
    elif (i, j) == (2, 3):
        positions.extend((depth+1, k, 4) for k in range(5))
    return positions


def recursive_get_dying(boards):
    dying = defaultdict(lambda: ([], []))
    for d1, board in list(boards.items()):
        for i1, j1 in zip(*np.where(board == '#')):
            n_adj_bugs = 0
            for d2, i2, j2 in recursive_adjacent_positions(d1, i1, j1):
                if d2 not in boards:
                    boards[d2] = np.full((5, 5), '.')
                if boards[d2][i2, j2] == '#':
                    n_adj_bugs += 1
            if n_adj_bugs != 1:
                dying[d1][0].append(i1)
                dying[d1][1].append(j1)
    return dying


def recursive_get_infesting(boards):
    infesting = defaultdict(lambda: ([], []))
    for d1, board in boards.items():
        for i1, j1 in zip(*np.where(board == '.')):
            if (i1, j1) == (2, 2):
                continue
            n_adj_bugs = 0
            for d2, i2, j2 in recursive_adjacent_positions(d1, i1, j1):
                if d2 in boards and boards[d2][i2, j2] == '#':
                    n_adj_bugs += 1
            if n_adj_bugs in {1, 2}:
                infesting[d1][0].append(i1)
                infesting[d1][1].append(j1)
    return infesting


boards = {0: np.array([list(x) for x in text.splitlines()])}
for _ in range(200):
    dying, infesting = recursive_get_dying(boards), recursive_get_infesting(boards)
    for depth, indices in dying.items():
        boards[depth][indices] = '.'
    for depth, indices in infesting.items():
        boards[depth][indices] = '#'
print(sum((b == '#').sum() for b in boards.values()))
