text = """
3,8,1001,8,10,8,105,1,0,0,21,46,67,88,101,126,207,288,369,450,99999,3,9,1001,9,5,9,1002,9,5,9,1001,9,5,9,102,3,9,9,101,2,9,9,4,9,99,3,9,102,4,9,9,101,5,9,9,102,5,9,9,101,3,9,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,102,3,9,9,1001,9,4,9,4,9,99,3,9,102,3,9,9,1001,9,3,9,1002,9,2,9,101,4,9,9,102,3,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,99
""".strip()


import pandas as pd
import itertools as it
from collections import deque


class Amplifier:
    def __init__(self, array):
        self.array = array
        self.i = 0
        self.input = deque()
        self.n_params = {
            99: 0,
            1: 3, 
            2: 3, 
            3: 1, 
            4: 1,
            5: 2,
            6: 2,
            7: 3,
            8: 3,
        }
        
    def run(self):
        a = self.array
        while True:
            instruction = "%05d" % a[self.i]
            opcode = int(instruction[3:])
            nparam = self.n_params[opcode]
            modes = [int(x) for x in list(instruction[:3])[::-1]]
            indices = [a[self.i+k+1] if modes[k] == 0 else self.i+k+1 for k in range(nparam)]
            auto_increase_pointer = True

            if opcode == 1:
                a[indices[2]] = a[indices[1]] + a[indices[0]]
            elif opcode == 2:
                a[indices[2]] = a[indices[1]] * a[indices[0]]
            elif opcode == 3:
                a[indices[0]] = self.input.popleft()
            elif opcode == 4:
                output = a[indices[0]]
                if output != 0:
                    self.i += nparam+1
                    return output
            elif opcode == 5:
                if a[indices[0]] != 0:
                    self.i = a[indices[1]]
                    auto_increase_pointer = False
            elif opcode == 6:
                if a[indices[0]] == 0:
                    self.i = a[indices[1]]
                    auto_increase_pointer = False
            elif opcode == 7:
                if a[indices[0]] < a[indices[1]]:
                    a[indices[2]] = 1
                else:
                    a[indices[2]] = 0
            elif opcode == 8:
                if a[indices[0]] == a[indices[1]]:
                    a[indices[2]] = 1
                else:
                    a[indices[2]] = 0
            elif opcode == 99:
                return None
            else:
                raise

            if auto_increase_pointer:
                self.i += nparam+1        


# 1
outputs = []
for phases in it.permutations(range(5)):
    array = pd.Series(text.split(','), dtype=int).values
    amplifiers = [Amplifier(array) for _ in range(5)]
    last_output = 0
    for amp, phs in zip(amplifiers, phases):
        amp.input.extend((phs, last_output))
        last_output = amp.run()
    outputs.append(last_output)
print(max(outputs))


# 2
outputs = []
for phases in it.permutations(range(5, 10)):
    array = pd.Series(text.split(','), dtype=int).values
    amplifiers = [Amplifier(array) for _ in range(5)]
    last_output = 0
    is_first_run = True
    while True:
        for amp, phs in zip(amplifiers, phases):
            if is_first_run:
                amp.input.extend((phs, last_output))
            else:
                amp.input.append(last_output)
            new_output = amp.run()
            if new_output is None:
                break
            last_output = new_output
        if new_output is None:
            break
        is_first_run = False
    outputs.append(last_output)
print(max(outputs))
