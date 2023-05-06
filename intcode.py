from collections import defaultdict

binops = {
    1: lambda x, y: x + y,
    2: lambda x, y: x * y,
    7: lambda x, y: x < y,
    8: lambda x, y: x == y,
}

instruction_lengths = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2}


class IntCodeProgram:
    def __init__(self, opcodes, inputs=None):
        program = defaultdict(int)
        for idx, opcode in enumerate(opcodes):
            program[idx] = int(opcode)
        self.initial_program = program
        self.program = program.copy()
        self.relative_base = 0
        self.ip = 0
        self.inputs = inputs if inputs is not None else []
        self.input_function = None

    def set_input(self, input_method):
        if callable(input_method):
            self.input_function = input_method
        else:
            self.inputs = input_method

    def get_input(self):
        if self.inputs:
            return self.inputs.pop(0)
        elif self.input_function:
            return self.input_function()

    def step(self):
        op = self.program[self.ip]
        instruction = op % 100
        l = instruction_lengths[instruction]
        vals = [self.program[x] for x in range(self.ip + 1, self.ip + l)]
        modes = [int(x) for x in str(op)[:-2].rjust(l - 1, "0")][::-1]
        offsets = [self.relative_base if mode == 2 else 0 for mode in modes]
        params = []
        for val, mode, offset in zip(vals, modes, offsets):
            params += [val if mode == 1 else self.program[val + offset]]
        if instruction in binops:
            dest = vals[2] + offsets[2]
            self.program[dest] = binops[instruction](*params[:-1])
        elif instruction == 3:
            dest = vals[0] + offsets[0]
            self.program[dest] = self.get_input()

        elif instruction == 4:
            self.ip += l
            return params[0]
        elif (instruction == 5 and params[0] != 0) or (
            instruction == 6 and params[0] == 0
        ):
            self.ip = params[1] - l
        elif instruction == 9:
            self.relative_base += params[0]
        self.ip += l
        return None

    def run(self):
        outputs = []
        ip = 0
        while (self.program[self.ip] % 100) != 99:
            output = self.step()
            if output is not None:
                yield output

    def reset(self):
        self.program = self.initial_program.copy()
        self.ip = 0
        self.relative_base = 0

    def copy(self):
        copy = IntCodeProgram([])
        copy.initial_program = self.initial_program.copy()
        copy.ip = self.ip
        copy.relative_base = self.relative_base
        copy.program = self.program.copy()
        return copy

    def set(self, position, value):
        self.program[position] = value
        self.initial_program[position] = value
