text = """
<x=-4, y=-9, z=-3>
<x=-13, y=-11, z=0>
<x=-17, y=-7, z=15>
<x=-16, y=4, z=2>
""".strip()


import re
import itertools as it
import numpy as np


class Moon:
    axes = ('x', 'y', 'z')
    def __init__(self, line):
        self.x, self.y, self.z = [int(x) for x in re.findall('-?\d+', line)]
        self.vx, self.vy, self.vz = 0, 0, 0
        
        
def get_state(moons, ax):
    return sum(tuple((getattr(m, ax), getattr(m, 'v' + ax)) for m in moons), ())


# 1        
moons = [Moon(line) for line in text.splitlines()]
N = 1000

for _ in range(N):
    for m1, m2 in it.combinations(moons, 2):
        for ax in Moon.axes:
            delta = np.sign(getattr(m2, ax) - getattr(m1, ax))
            setattr(m2, 'v' + ax, getattr(m2, 'v' + ax) - delta)
            setattr(m1, 'v' + ax, getattr(m1, 'v' + ax) + delta)
    for m in moons:
        for ax in Moon.axes:
            setattr(m, ax, getattr(m, ax) + getattr(m, 'v' + ax))
    
energy = 0
for m in moons:
    pot = sum(abs(getattr(m, ax)) for ax in Moon.axes)
    kin = sum(abs(getattr(m, 'v' + ax)) for ax in Moon.axes)
    energy += pot * kin
print(energy)


# 2
moons = [Moon(line) for line in text.splitlines()]
periods = []

for ax in Moon.axes:
    previous_states = set()
    i = 0
    while True:
        for m1, m2 in it.combinations(moons, 2):
            delta = np.sign(getattr(m2, ax) - getattr(m1, ax))
            setattr(m2, 'v' + ax, getattr(m2, 'v' + ax) - delta)
            setattr(m1, 'v' + ax, getattr(m1, 'v' + ax) + delta)
        for m in moons:
            setattr(m, ax, getattr(m, ax) + getattr(m, 'v' + ax))
        state = get_state(moons, ax)
        if state in previous_states:
            break
        else:
            previous_states.add(state)
        i += 1
    periods.append(i)

print(np.lcm.reduce(periods))
