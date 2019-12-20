text = """
109,424,203,1,21101,11,0,0,1105,1,282,21102,18,1,0,1105,1,259,1201,1,0,221,203,1,21102,1,31,0,1105,1,282,21101,38,0,0,1105,1,259,20102,1,23,2,21202,1,1,3,21102,1,1,1,21101,0,57,0,1106,0,303,1201,1,0,222,21001,221,0,3,21002,221,1,2,21101,0,259,1,21102,80,1,0,1106,0,225,21102,1,93,2,21101,0,91,0,1105,1,303,2102,1,1,223,21002,222,1,4,21101,0,259,3,21102,225,1,2,21101,0,225,1,21102,1,118,0,1105,1,225,21001,222,0,3,21101,0,73,2,21101,133,0,0,1105,1,303,21202,1,-1,1,22001,223,1,1,21101,148,0,0,1106,0,259,2102,1,1,223,20101,0,221,4,21001,222,0,3,21102,1,11,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21102,195,1,0,105,1,109,20207,1,223,2,21002,23,1,1,21101,-1,0,3,21101,214,0,0,1105,1,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,2101,0,-4,249,22101,0,-3,1,22101,0,-2,2,21201,-1,0,3,21101,250,0,0,1106,0,225,22101,0,1,-4,109,-5,2106,0,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2105,1,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,22101,0,-2,-2,109,-3,2105,1,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,21202,-2,1,3,21102,1,343,0,1106,0,303,1106,0,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,22101,0,-4,1,21102,1,384,0,1105,1,303,1105,1,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,21202,1,1,-4,109,-5,2105,1,0
""".strip()


import numpy as np
import itertools as it
from collections import deque


class Computer:
    num_parameters = {
        99: 0,
        1: 3, 
        2: 3, 
        3: 1, 
        4: 1,
        5: 2,
        6: 2,
        7: 3,
        8: 3,
        9: 1,
    }
    
    def __init__(self, program, memory_size=10000):
        self.memory = list(program).copy() + [0] * (memory_size - len(program))
        self.instruction_pointer = 0
        self.relative_base = 0
        self.inputs = deque()
        self.outputs = deque()
        
    def add_inputs(self, inputs):
        try:
            iter(inputs)
        except:
            inputs = [inputs]
        self.inputs.extend(inputs)
        return self
    
    def pop_output(self):
        return self.outputs.popleft()
    
    def interpret_indices(self, nparam, modes):
        indices = []
        for k in range(nparam):
            if modes[k] == 0:
                indices.append(self.memory[self.instruction_pointer+k+1])
            elif modes[k] == 1:
                indices.append(self.instruction_pointer+k+1)
            elif modes[k] == 2:
                indices.append(self.memory[self.instruction_pointer+k+1] + self.relative_base)
        return indices
    
    def apply_instruction(self, opcode, indices, nparam, wait_for_input):
        increase_pointer = True
        
        if opcode == 99:
            return True
        elif opcode == 1:
            self.memory[indices[2]] = self.memory[indices[1]] + self.memory[indices[0]]
        elif opcode == 2:
            self.memory[indices[2]] = self.memory[indices[1]] * self.memory[indices[0]]
        elif opcode == 3:
            try:
                self.memory[indices[0]] = self.inputs.popleft()
            except IndexError as e:
                if wait_for_input:
                    return True
                raise e
        elif opcode == 4:
            self.outputs.append(self.memory[indices[0]])
        elif opcode == 5:
            if self.memory[indices[0]] != 0:
                self.instruction_pointer = self.memory[indices[1]]
                increase_pointer = False
        elif opcode == 6:
            if self.memory[indices[0]] == 0:
                self.instruction_pointer = self.memory[indices[1]]
                increase_pointer = False
        elif opcode == 7:
            self.memory[indices[2]] = 1 if self.memory[indices[0]] < self.memory[indices[1]] else 0
        elif opcode == 8:
            self.memory[indices[2]] = 1 if self.memory[indices[0]] == self.memory[indices[1]] else 0
        elif opcode == 9:
            self.relative_base += self.memory[indices[0]]

        if increase_pointer:
            self.instruction_pointer += nparam+1
        return False
        
    def run(self, n_outputs=np.inf, wait_for_input=False):
        halt = False
        while not halt:
            instruction = "%05d" % self.memory[self.instruction_pointer]
            opcode = int(instruction[3:])
            nparam = self.num_parameters[opcode]
            modes = [int(x) for x in list(instruction[:3])[::-1]]
            indices = self.interpret_indices(nparam, modes)
            halt = self.apply_instruction(opcode, indices, nparam, wait_for_input)
            if len(self.outputs) >= n_outputs:
                break
        return halt

    
# 1
program = list(int(x) for x in text.split(','))
outputs = []
for x, y in it.product(range(50), repeat=2):
    computer = Computer(program)
    computer.add_inputs([x, y])
    computer.run()
    outputs.append(computer.pop_output())
print((np.array(outputs) == 1).sum())


# 2
def get_diagonal_size(i, j):
    diagonal_size = 0
    # Top right diagonal
    i2, j2 = i, j
    while True:
        computer = Computer(program).add_inputs([i2, j2])
        computer.run()
        out = computer.pop_output()
        if out == 0:
            break
        i2, j2, diagonal_size = i2-1, j2+1, diagonal_size+1
    # Bottom left diagonal
    i2, j2 = i+1, j-1
    while True:
        computer = Computer(program).add_inputs([i2, j2])
        computer.run()
        out = computer.pop_output()
        if out == 0:
            break
        i2, j2, diagonal_size = i2+1, j2-1, diagonal_size+1
    return diagonal_size


def incremental_check(diagonal_sizes, delta_i, delta_j, delta_step):
    step = 0
    while True:
        step += delta_step
        i, j = int(delta_i*step), int(delta_j*step)
        diagonal_size = get_diagonal_size(i, j)
        diagonal_sizes[(i, j)] = diagonal_size
        if diagonal_size >= square_size:
            break

            
def dichotomy_check(diagonal_sizes):
    (i2, j2), (i1, j1) = sorted(diagonal_sizes, key=lambda k: diagonal_sizes[k], reverse=True)[:2]
    while True:
        i, j = (i1+i2)//2, (j1+j2)//2
        if (i, j) in diagonal_sizes:
            break
        diagonal_size = get_diagonal_size(i, j)
        diagonal_sizes[(i, j)] = diagonal_size
        if diagonal_size < square_size:
            i1, j1 = i, j
        else:
            i2, j2 = i, j

            
def get_top_left_of_square(i_diag, j_diag):
    i2, j2 = i_diag, j_diag
    while True:
        computer = Computer(program).add_inputs([i2, j2])
        computer.run()
        out = computer.pop_output()
        if out == 0:
            break
        i2, j2 = i2-1, j2+1
    return i2+1, j2-square_size


square_size = 100
board = np.array(outputs).reshape(50, 50)
delta_i = np.where((board == 1).any(axis=1) & (board[:, -1] == 0))[0][-1]
delta_j = (np.where(board[delta_i] == 1)[0][[0, -1]]).mean()

diagonal_sizes = dict()
incremental_check(diagonal_sizes, delta_i, delta_j, delta_step=5)
dichotomy_check(diagonal_sizes)
i_diagonal, j_diagonal = min((k for k, v in diagonal_sizes.items() if v >= square_size))
i, j = get_top_left_of_square(i_diagonal, j_diagonal)
print(i*10000+j)
