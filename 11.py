text = """
3,8,1005,8,304,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,1002,8,1,29,2,103,1,10,1,106,18,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,59,2,102,3,10,2,1101,12,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,88,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,101,0,8,110,2,108,9,10,1006,0,56,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,139,1,108,20,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,165,1,104,9,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,192,2,9,14,10,2,1103,5,10,1,1108,5,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,102,1,8,226,1006,0,73,1006,0,20,1,1106,11,10,1,1105,7,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,261,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,283,101,1,9,9,1007,9,1052,10,1005,10,15,99,109,626,104,0,104,1,21101,48062899092,0,1,21101,0,321,0,1105,1,425,21101,936995300108,0,1,21101,0,332,0,1106,0,425,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,209382902951,1,1,21101,379,0,0,1106,0,425,21102,179544747200,1,1,21102,390,1,0,1106,0,425,3,10,104,0,104,0,3,10,104,0,104,0,21102,1,709488292628,1,21102,1,413,0,1106,0,425,21101,0,983929868648,1,21101,424,0,0,1105,1,425,99,109,2,22101,0,-1,1,21102,40,1,2,21102,456,1,3,21101,446,0,0,1106,0,489,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,451,452,467,4,0,1001,451,1,451,108,4,451,10,1006,10,483,1102,0,1,451,109,-2,2105,1,0,0,109,4,1201,-1,0,488,1207,-3,0,10,1006,10,506,21102,1,0,-3,21202,-3,1,1,21201,-2,0,2,21101,0,1,3,21101,525,0,0,1105,1,530,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,553,2207,-4,-2,10,1006,10,553,21202,-4,1,-4,1105,1,621,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,1,572,0,1106,0,530,21201,1,0,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,591,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,613,22101,0,-1,1,21101,0,613,0,106,0,488,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0
""".strip()


import numpy as np
from collections import deque
import matplotlib.pyplot as plt


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
    
    def apply_instruction(self, opcode, indices, nparam):
        increase_pointer = True
        
        if opcode == 99:
            return True
        elif opcode == 1:
            self.memory[indices[2]] = self.memory[indices[1]] + self.memory[indices[0]]
        elif opcode == 2:
            self.memory[indices[2]] = self.memory[indices[1]] * self.memory[indices[0]]
        elif opcode == 3:
            self.memory[indices[0]] = self.inputs.popleft()
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
        
    def run(self, n_outputs=np.inf):
        halt = False
        while not halt:
            instruction = "%05d" % self.memory[self.instruction_pointer]
            opcode = int(instruction[3:])
            nparam = self.num_parameters[opcode]
            modes = [int(x) for x in list(instruction[:3])[::-1]]
            indices = self.interpret_indices(nparam, modes)
            halt = self.apply_instruction(opcode, indices, nparam)
            if len(self.outputs) >= n_outputs:
                break
        return halt


def build_empty_panels(size, first_color):
    panels = np.empty((size, size), str)
    i, j = size//2, size//2
    panels[i, j] = first_color
    return panels, i, j


def paint_panels(panels, computer, start_i, start_j, start_direction):
    i, j, direction = start_i, start_j, start_direction

    while True:
        computer.add_inputs(0 if panels[i, j] in {'.', ''} else 1)
        halt = computer.run(n_outputs=2)
        if halt:
            break

        first_output = computer.pop_output()
        panels[i, j] = '.' if first_output == 0 else '#'

        second_output = computer.pop_output()
        side = 'left' if second_output == 0 else 'right'
        direction = rotate(direction, side)
        i, j = move_one_step(i, j, direction)

    return panels


def rotate(previous_direction, side):
    d = {
        'up': {'right': 'right', 'left': 'left'},
        'right': {'right': 'down', 'left': 'up'},
        'down': {'right': 'left', 'left': 'right'},
        'left': {'right': 'up', 'left': 'down'},
    }
    return d[previous_direction][side]


def move_one_step(i, j, direction):
    d = {
        'up': (i-1, j),
        'right': (i, j+1),
        'down': (i+1, j),
        'left': (i, j-1),
    }
    return d[direction]
    

def plot_panels(panels):
    img = panels.copy()
    img[(img == '') | (img == '.')] = '0'
    img[img == '#'] = '1'
    img = img.astype(int)
    plt.imshow(img, cmap='gray')
    plt.show()

    
# 1
program = [int(x) for x in text.split(',')]
computer = Computer(program)
panels, i, j = build_empty_panels(size=500, first_color='.')
panels = paint_panels(panels, computer, i, j, 'up')
print((panels != '').sum())


# 2
program = [int(x) for x in text.split(',')]
computer = Computer(program)
panels, i, j = build_empty_panels(size=85, first_color='#')
panels = paint_panels(panels, computer, i, j, 'up')
plot_panels(panels)
