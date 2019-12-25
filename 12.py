text = """
<x=-4, y=-9, z=-3>
<x=-13, y=-11, z=0>
<x=-17, y=-7, z=15>
<x=-16, y=4, z=2>
""".strip()


import re
import numba as nb
import numpy as np


class Moon:
    def __init__(self, line):
        x, y, z = [int(x) for x in re.findall('-?\d+', line)]
        self.position = [x, y, z]
        self.velocity = [0, 0, 0]
        

@nb.njit
def update_axe_for_one_step(positions, velocities, n):
    for i1 in range(n):
        for i2 in range(i1, n):
            delta = np.sign(positions[i1] - positions[i2])
            velocities[i1] -= delta
            velocities[i2] += delta
    for i in range(n):
        positions[i] += velocities[i]
        

@nb.njit
def update_axe(positions, velocities, steps):
    n = len(positions)
    for _ in range(steps):
        update_axe_for_one_step(positions, velocities, n)
        

@nb.njit
def update_axe_until_repetition(positions, velocities):
    n = len(positions)
    initial_state = positions + velocities
    step = 0
    while True:
        step += 1
        update_axe_for_one_step(positions, velocities, n)
        new_state = positions + velocities
        if new_state == initial_state:
            return step


# 1
moons = [Moon(line) for line in text.splitlines()]
steps = 1000

for i in range(3):
    positions = [m.position[i] for m in moons]
    velocities = [m.velocity[i] for m in moons]
    update_axe(positions, velocities, steps)
    for j, m in enumerate(moons):
        m.position[i] = positions[j]
        m.velocity[i] = velocities[j]
print(sum(sum(abs(x) for x in m.position) * sum(abs(x) for x in m.velocity) for m in moons))


# 2
moons = [Moon(line) for line in text.splitlines()]
periods = []
for i in range(3):
    positions = [m.position[i] for m in moons]
    velocities = [m.velocity[i] for m in moons]
    periods.append(update_axe_until_repetition(positions, velocities))
print(np.lcm.reduce(periods))
