text = """
.#....#.###.........#..##.###.#.....##...
...........##.......#.#...#...#..#....#..
...#....##..##.......#..........###..#...
....#....####......#..#.#........#.......
...............##..#....#...##..#...#..#.
..#....#....#..#.....#.#......#..#...#...
.....#.#....#.#...##.........#...#.......
#...##.#.#...#.......#....#........#.....
....##........#....#..........#.......#..
..##..........##.....#....#.........#....
...#..##......#..#.#.#...#...............
..#.##.........#...#.#.....#........#....
#.#.#.#......#.#...##...#.........##....#
.#....#..#.....#.#......##.##...#.......#
..#..##.....#..#.........#...##.....#..#.
##.#...#.#.#.#.#.#.........#..#...#.##...
.#.....#......##..#.#..#....#....#####...
........#...##...#.....#.......#....#.#.#
#......#..#..#.#.#....##..#......###.....
............#..#.#.#....#.....##..#......
...#.#.....#..#.......#..#.#............#
.#.#.....#..##.....#..#..............#...
.#.#....##.....#......##..#...#......#...
.......#..........#.###....#.#...##.#....
.....##.#..#.....#.#.#......#...##..#.#..
.#....#...#.#.#.......##.#.........#.#...
##.........#............#.#......#....#..
.#......#.............#.#......#.........
.......#...##........#...##......#....#..
#..#.....#.#...##.#.#......##...#.#..#...
#....##...#.#........#..........##.......
..#.#.....#.....###.#..#.........#......#
......##.#...#.#..#..#.##..............#.
.......##.#..#.#.............#..#.#......
...#....##.##..#..#..#.....#...##.#......
#....#..#.#....#...###...#.#.......#.....
.#..#...#......##.#..#..#........#....#..
..#.##.#...#......###.....#.#........##..
#.##.###.........#...##.....#..#....#.#..
..........#...#..##..#..##....#.........#
..#..#....###..........##..#...#...#..#..
""".strip()


import math
import numpy as np
import pandas as pd
from collections import Counter, deque


def get_angle(i1, j1, i2, j2):
    angle_radians = math.atan2(j2-j1, i1-i2)
    if angle_radians < 0.0:
        angle_radians += 2*math.pi;
    return round(math.degrees(angle_radians), 9)


array = np.array([list(x) for x in text.splitlines()])
asteroid_positions = list(zip(*np.where(array == '#')))


# 1
scores = dict()
for i, j in asteroid_positions:
    angles = [get_angle(i, j, i1, j1) for i1, j1 in asteroid_positions if (i1, j1) != (i, j)]
    scores[(i, j)] = len(Counter(angles))
i0, j0 = max(scores, key=lambda k: scores[k])
print(scores[i0, j0])


# 1 bis (faster)
# N = len(asteroid_positions)
# i, j = np.array(asteroid_positions).T
# cross_i = np.transpose([np.tile(i, N), np.repeat(i, N)])
# cross_j = np.transpose([np.tile(j, N), np.repeat(j, N)])
# delta_x = cross_i[:, 0] - cross_i[:, 1]
# delta_y = cross_j[:, 1] - cross_j[:, 0]
# angles = np.arctan2(delta_y, delta_x).reshape(N, N)
# num_unique_angles = [np.unique(row).size for row in angles]
# best_ind = np.argmax(num_unique_angles)
# i0, j0 = asteroid_positions[best_ind]
# print(num_unique_angles[best_ind])


# 2
angles = {(i, j): get_angle(i0, j0, i, j) for i, j in asteroid_positions if (i, j) != (i0, j0)}
i_distances = {(i, j): abs(i-i0) for i, j in asteroid_positions if (i, j) != (i0, j0)}
queue = deque(pd.DataFrame([angles, i_distances]).T.sort_values([0, 1]).reset_index().values)

def contains_other_angles(queue, angle):
    angles = set(np.array(list(queue))[:, 1])
    angles.add(angle)
    return len(angles) > 1

results = []
previous_angle = -1
while queue:
    x = queue.popleft()
    (i, j), angle, distance = x
    if angle == previous_angle and queue and contains_other_angles(queue, angle):
        queue.append(x)
        continue
    results.append((i, j))
    previous_angle = angle
print(results[199][1] * 100 + results[199][0])
