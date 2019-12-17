import asyncio

from collections import defaultdict


def get_program():
    with open('../33/input', 'rt') as f:
        intcode = [int(i.strip()) for i in f.read().strip().split(',')]

    intcode_dict = defaultdict(int)
    intcode_dict.update({index: code for index, code in enumerate(intcode)})

    return [intcode_dict, 0]   # code, instruction pointer


async def run_program(program, in_queue, out_queue, prog_name=None):

    intcode, instruction_pointer = program

    relative_base = 0

    while True:
        opcode = intcode[instruction_pointer]
        opcode = str(opcode).zfill(5)
        a_mode = int(opcode[2])
        b_mode = int(opcode[1])
        c_mode = int(opcode[0])
        opcode = int(opcode[3:].lstrip('0'))

        #print(instruction_pointer, opcode)

        if opcode == 1:
            a_ptr = intcode[instruction_pointer+1]
            b_ptr = intcode[instruction_pointer+2]
            c_ptr = intcode[instruction_pointer+3]

            if a_mode == 0:
                a_ptr = intcode[a_ptr]
            elif a_mode == 2:
                a_ptr = intcode[relative_base + a_ptr]

            if b_mode == 0:
                b_ptr = intcode[b_ptr]
            elif b_mode == 2:
                b_ptr = intcode[relative_base + b_ptr]

            if c_mode == 0:
                pass
            elif c_mode == 2:
                c_ptr += relative_base

            result = a_ptr + b_ptr
            intcode[c_ptr] = result

            instruction_pointer += 4

        elif opcode == 2:
            a_ptr = intcode[instruction_pointer+1]
            b_ptr = intcode[instruction_pointer+2]
            c_ptr = intcode[instruction_pointer+3]

            if a_mode == 0:
                a_ptr = intcode[a_ptr]
            elif a_mode == 2:
                a_ptr = intcode[relative_base + a_ptr]

            if b_mode == 0:
                b_ptr = intcode[b_ptr]
            elif b_mode == 2:
                b_ptr = intcode[relative_base + b_ptr]

            if c_mode == 0:
                pass
            elif c_mode == 2:
                c_ptr += relative_base

            result = a_ptr * b_ptr
            intcode[c_ptr] = result

            instruction_pointer += 4

        elif opcode == 3:
            a_ptr = intcode[instruction_pointer+1]

            if a_mode == 0:
                pass
            elif a_mode == 2:
                a_ptr += relative_base

            await out_queue.put('input')   # signal that we need input
            input_ = await in_queue.get()
            intcode[a_ptr] = input_

            if prog_name:
                print(prog_name, 'got input', input_)

            instruction_pointer += 2

        elif opcode == 4:
            a_ptr = intcode[instruction_pointer+1]

            if a_mode == 0:
                output = intcode[a_ptr]
            elif a_mode == 2:
                output = intcode[relative_base + a_ptr]
            else:
                output = a_ptr

            instruction_pointer += 2

            program[1] = instruction_pointer
            await out_queue.put(output)

            if prog_name:
                print(prog_name, 'output', output)

        elif opcode == 5:
            a_ptr = intcode[instruction_pointer+1]
            b_ptr = intcode[instruction_pointer+2]

            if a_mode == 0:
                a_ptr = intcode[a_ptr]
            elif a_mode == 2:
                a_ptr = intcode[relative_base + a_ptr]

            if b_mode == 0:
                b_ptr = intcode[b_ptr]
            elif b_mode == 2:
                b_ptr = intcode[relative_base + b_ptr]

            if a_ptr != 0:
                instruction_pointer = b_ptr
            else:
                instruction_pointer += 3

        elif opcode == 6:
            a_ptr = intcode[instruction_pointer+1]
            b_ptr = intcode[instruction_pointer+2]

            if a_mode == 0:
                a_ptr = intcode[a_ptr]
            elif a_mode == 2:
                a_ptr = intcode[relative_base + a_ptr]

            if b_mode == 0:
                b_ptr = intcode[b_ptr]
            elif b_mode == 2:
                b_ptr = intcode[relative_base + b_ptr]

            if a_ptr == 0:
                instruction_pointer = b_ptr
            else:
                instruction_pointer += 3

        elif opcode == 7:
            a_ptr = intcode[instruction_pointer+1]
            b_ptr = intcode[instruction_pointer+2]
            c_ptr = intcode[instruction_pointer+3]

            if a_mode == 0:
                a_ptr = intcode[a_ptr]
            elif a_mode == 2:
                a_ptr = intcode[relative_base + a_ptr]

            if b_mode == 0:
                b_ptr = intcode[b_ptr]
            elif b_mode == 2:
                b_ptr = intcode[relative_base + b_ptr]

            if c_mode == 0:
                pass
            elif c_mode == 2:
                c_ptr += relative_base

            if a_ptr < b_ptr:
                intcode[c_ptr] = 1
            else:
                intcode[c_ptr] = 0

            instruction_pointer += 4

        elif opcode == 8:
            a_ptr = intcode[instruction_pointer+1]
            b_ptr = intcode[instruction_pointer+2]
            c_ptr = intcode[instruction_pointer+3]

            if a_mode == 0:
                a_ptr = intcode[a_ptr]
            elif a_mode == 2:
                a_ptr = intcode[relative_base + a_ptr]

            if b_mode == 0:
                b_ptr = intcode[b_ptr]
            elif b_mode == 2:
                b_ptr = intcode[relative_base + b_ptr]

            if c_mode == 0:
                pass
            elif c_mode == 2:
                c_ptr += relative_base

            if a_ptr == b_ptr:
                intcode[c_ptr] = 1
            else:
                intcode[c_ptr] = 0

            instruction_pointer += 4

        elif opcode == 9:
            a_ptr = intcode[instruction_pointer+1]

            if a_mode == 0:
                a_ptr = intcode[a_ptr]
            elif a_mode == 2:
                a_ptr = intcode[relative_base + a_ptr]

            relative_base += a_ptr

            instruction_pointer += 2

        elif opcode == 99:
            break

        else:
            raise Exception('?')

    program[1] = instruction_pointer
    await out_queue.put(None)   # <-- signal end-of-program

    if prog_name:
        print(prog_name, 'terminated')


async def io_1(in_queue, out_queue):
    #await in_queue.put(thing)
    m = []
    row = []
    while True:
        thing = await out_queue.get()
        if thing is None:
            break
        thing = str(chr(thing))
        if thing == '\n':
            if row:
                m.append(row)
            row = []
        else:
            row.append(thing)

    return m


async def io_2(in_queue, out_queue, commands):
    #await in_queue.put(thing)
    #thing = await out_queue.get()
    groups, order = commands

    for c in order:
        await in_queue.put(c)

    for group in groups:
        for c in group:
            await in_queue.put(c)

    await in_queue.put(ord('n'))
    await in_queue.put(ord('\n'))

    score = None

    m = []
    row = []
    while True:
        thing = await out_queue.get()
        if thing is None:
            break
        if thing == 'input':
            continue
        if thing > 255:
            score = thing
            continue
        thing = str(chr(thing))
        if thing == '\n':
            if row:
                m.append(row)
            row = []
        else:
            row.append(thing)

    for row in m:
        print(''.join(row))

    print('SCORE', score)


async def solve():

    program = get_program()

    program[0][0] = 1

    in_queue = asyncio.Queue()
    out_queue = asyncio.Queue()

    io_task = asyncio.create_task(io_1(in_queue, out_queue))
    prog_task = asyncio.create_task(run_program(program, in_queue, out_queue))

    m = await io_task
    _ = await prog_task

    for row in m:
        print(''.join(row))

    path = walk_path(m)

    commands = group_moves(path)

    program = get_program()

    program[0][0] = 2

    in_queue = asyncio.Queue()
    out_queue = asyncio.Queue()

    io_task = asyncio.create_task(io_2(in_queue, out_queue, commands))
    prog_task = asyncio.create_task(run_program(program, in_queue, out_queue))

    _ = await io_task
    _ = await prog_task


import copy


def find_robot(m):
    for y, row in enumerate(m):
        for x, val in enumerate(row):
            if val in ('^', '<', '>', 'v'):
                return x, y, val


def walk_path(m):
    m = copy.deepcopy(m)
    x, y, val = find_robot(m)

    print('Robot starts at:', x, y, val)

    # I looked at the map and it's pretty simple. It's clearly one path and you can go as far in one direction as you need,
    # turn, keep going, and you never need to backtrack. So we'll use this fact.

    turns = {
            '^': {
                'right': 'R',
                'left': 'L',
            },
            '>': {
                'down': 'R',
                'up': 'L',
            },
            'v': {
                'left': 'R',
                'right': 'L',
            },
            '<': {
                'up': 'R',
                'down': 'L',
            },
    }

    path = []

    while True:
        dist = 0

        # Each loop here does one turn and then one movement as far as it can go.
        if x+1 < len(m[y]) and m[y][x+1] == '#':
            direction = turns[val]['right']
            val = '>'
            while x+1 < len(m[y]) and m[y][x+1] in ('#', 'o'):
                dist += 1
                m[y][x] = 'o'
                x += 1

        elif x > 0 and m[y][x-1] == '#':
            direction = turns[val]['left']
            val = '<'
            while x > 0 and m[y][x-1] in ('#', 'o'):
                dist += 1
                m[y][x] = 'o'
                x -= 1

        elif y+1 < len(m) and m[y+1][x] == '#':
            direction = turns[val]['down']
            val = 'v'
            while y+1 < len(m) and m[y+1][x] in ('#', 'o'):
                dist += 1
                m[y][x] = 'o'
                y += 1

        elif y > 0 and  m[y-1][x] == '#':
            direction = turns[val]['up']
            val = '^'
            while y > 0 and m[y-1][x] in ('#', 'o'):
                dist += 1
                m[y][x] = 'o'
                y -= 1

        else:
            break

        path.append(direction)
        path.append(dist)


    for row in m:
        print(''.join(row))

    print(len(path), path)
    return path


from collections import Counter
import random


def encode_command(group):
    encoded = []
    for i, c in enumerate(group):
        if i > 0:
            encoded.append(ord(','))
        if c in ('L', 'R', 'A', 'B', 'C'):
            encoded.append(ord(c))
        else:
            encoded.extend([ord(s) for s in str(c)])
    encoded.append(ord('\n'))
    return encoded


def group_moves(path):
    possible_groups = []

    for i in range(0, len(path), 2):
        for size in (4, 6, 8, 10):
            group = tuple(path[i:i+size])
            if len(encode_command(group)) <= 21:
                possible_groups.append(group)

    okay_groups = []

    for group, count in Counter(possible_groups).most_common():
        if count > 1:
            okay_groups.append(group)

    while True:
        groups = random.sample(okay_groups, 3)

        order = []

        i = 0

        try:
            while i < len(path):
                for g_index, g in enumerate(groups):
                    l = len(g)
                    if tuple(path[i:i+l]) == g:
                        i += l
                        order.append(g_index)
                        break
                else:
                    raise Exception('does not work')
        except:
            continue

        break

    order = [('A', 'B', 'C')[o] for o in order]

    return [encode_command(g) for g in groups], encode_command(order)


if __name__ == '__main__':
    asyncio.run(solve())

