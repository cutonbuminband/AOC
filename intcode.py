binops = {
    1: lambda x, y: x + y,
    2: lambda x, y: x * y,
    7: lambda x, y: x < y,
    8: lambda x, y: x == y,
}

instruction_lengths = {1: 4, 2: 4, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 2}


def step(program, ip, inputs=None, outputs=None, relative_base=0):
    op = program[ip]
    instruction = op % 100
    l = instruction_lengths[instruction]
    vals = [program[x] for x in range(ip + 1, ip + l)]
    modes = [int(x) for x in str(op)[:-2].rjust(l - 1, "0")][::-1]
    offsets = [relative_base if mode == 2 else 0 for mode in modes]
    params = []
    for val, mode, offset in zip(vals, modes, offsets):
        params += [val if mode == 1 else program[val + offset]]
    if instruction in binops:
        dest = vals[2] + offsets[2]
        program[dest] = binops[instruction](*params[:-1])
    elif instruction == 3:
        dest = vals[0] + offsets[0]
        if inputs is None:
            program[dest] = int(input("Please input the parameter\n"))
        elif inputs:
            program[dest] = inputs.pop(0)
        else:
            ip -= l

    elif instruction == 4:
        if outputs is None:
            print("Program output: {}".format(params[0]))
        else:
            outputs.append(params[0])
    elif (instruction == 5 and params[0] != 0) or (instruction == 6 and params[0] == 0):
        ip = params[1] - l
    elif instruction == 9:
        relative_base += params[0]
    return program, ip + l, relative_base


def run(program, inputs=None, relative_base=0):
    outputs = []
    ip = 0
    while (program[ip] % 100) != 99:
        program, ip, relative_base = step(program, ip, inputs, outputs, relative_base)
        if outputs:
            yield outputs.pop()
