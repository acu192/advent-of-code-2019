import sys
import string
import asyncio

from itertools import combinations
from collections import defaultdict


ASCII_OUTPUT = True


ASCII_PRINTABLE_INTEGERS = set([ord(c) for c in string.printable])


def get_program():
    global _PROGRAM_SOURCE

    try:
        _PROGRAM_SOURCE
    except NameError:
        with open('input', 'rt') as f:
            first_line = f.read()
        _PROGRAM_SOURCE = [int(i.strip()) for i in first_line.strip().split(',')]

    intcode_dict = defaultdict(int)
    intcode_dict.update({index: code for index, code in enumerate(_PROGRAM_SOURCE)})

    return [intcode_dict, 0]   # code, instruction pointer


async def run_program(program, in_queue, out_queue, prog_name=None, signal_for_input=False):

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

            if signal_for_input:
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


async def io(in_queue, out_queue):
    loop = asyncio.get_running_loop()

    async def write_to_stdout():
        while True:
            c = await out_queue.get()
            if c is None:
                break
            if ASCII_OUTPUT:
                if c in ASCII_PRINTABLE_INTEGERS:
                    c = chr(c)
                    print(c, end='', flush=True)
                else:
                    print('\nNON-PRINTABLE OUTPUT:', c, '\n')
            else:
                print('OUTPUT:', c)

    async def read_from_stdin():
        while True:
            line = await loop.run_in_executor(
                    None,
                    sys.stdin.readline,
                    # no params...
            )
            for c in line:
                c = ord(c)
                await in_queue.put(c)

    write_task = asyncio.create_task(write_to_stdout())
    read_task = asyncio.create_task(read_from_stdin())

    await write_task

    read_task.cancel()
    try:
        await read_task
    except asyncio.CancelledError:
        # We expect this.
        pass


async def readline(out_queue):
    stuff = []
    term = False

    while True:
        thing = await out_queue.get()

        if thing is None:
            term = True
            break

        elif thing == 10:  # new line
            break

        else:
            stuff.append(chr(thing))

    return ''.join(stuff), term


async def readsection(out_queue):
    name = None
    doors = []
    items = []

    print('CALLING READ_SECTION')

    while True:
        line, term = await readline(out_queue)
        print('>>>', line)

        if term:
            print('TERMINATING')
            sys.exit(1)

        if line.startswith('== '):
            name = line

        if line == 'Doors here lead:':
            while True:
                line, term = await readline(out_queue)
                print('>>>', line)
                if line == '':
                    break
                line = line.lstrip(' -')
                doors.append(line)

        if line == 'Items here:':
            while True:
                line, term = await readline(out_queue)
                print('>>>', line)
                if line == '':
                    break
                line = line.lstrip(' -')
                items.append(line)

        if line == 'Command?':
            break

    return name, doors, items


async def go(in_queue, direction):
    for c in direction:
        await in_queue.put(ord(c))
    await in_queue.put(10)  # new line


async def take(in_queue, item):
    item = 'take {}'.format(item)
    for c in item:
        await in_queue.put(ord(c))
    await in_queue.put(10)  # new line


async def drop(in_queue, item):
    item = 'drop {}'.format(item)
    for c in item:
        await in_queue.put(ord(c))
    await in_queue.put(10)  # new line


def reversedoor(direction):
    return {
            'north': 'south',
            'south': 'north',
            'east': 'west',
            'west': 'east',
    }[direction]


async def explore(in_queue, out_queue, visited):
    #await in_queue.put(thing)
    #thing = await out_queue.get()

    name, doors, items = await readsection(out_queue)

    if name in visited:
        return

    visited.add(name)

    for item in items:
        if item not in ('giant electromagnet', 'molten lava', 'photons', 'escape pod', 'infinite loop'):
            await take(in_queue, item)
            _ = await readsection(out_queue)

    if name == '== Security Checkpoint ==':
        return

    for door in doors:
        await go(in_queue, door)
        print('Going', door)

        await explore(in_queue, out_queue, visited)

        await go(in_queue, reversedoor(door))
        print('Reversing', door)

        _ = await readsection(out_queue)


async def get_inv(in_queue, out_queue):
    for c in 'inv':
        await in_queue.put(ord(c))
    await in_queue.put(10)  # new line

    inv = []

    while True:
        line, term = await readline(out_queue)
        print('>>>', line)

        if line == 'Items in your inventory:':
            while True:
                line, term = await readline(out_queue)
                print('>>>', line)
                if line == '':
                    break
                line = line.lstrip(' -')
                inv.append(line)

        elif line == 'Command?' and inv:
            break

    return inv


async def explore_root(in_queue, out_queue):
    visited = set()

    await explore(in_queue, out_queue, visited)

    await go(in_queue, 'north')
    await go(in_queue, 'north')
    await go(in_queue, 'east')

    inv = await get_inv(in_queue, out_queue)

    print('INVENTORY!', inv)

    found = False

    for r in range(1, len(inv)+1):
        for combo in combinations(inv, r):
            for thing in inv:
                await drop(in_queue, thing)
                _ = await readsection(out_queue)
            for thing in combo:
                await take(in_queue, thing)
                _ = await readsection(out_queue)
            await go(in_queue, 'south')
            name, doors, items = await readsection(out_queue)
            if name != '== Security Checkpoint ==':
                found = True
                break
        if found:
            break

    await io(in_queue, out_queue)


async def solve():

    program = get_program()

    in_queue = asyncio.Queue()
    out_queue = asyncio.Queue(maxsize=1)

    CMDLINE = False # True

    if CMDLINE:
        io_task = asyncio.create_task(io(in_queue, out_queue))
        signal_for_input = False

    else:
        io_task = asyncio.create_task(explore_root(in_queue, out_queue))
        signal_for_input = False

    prog_task = asyncio.create_task(run_program(program, in_queue, out_queue, signal_for_input=signal_for_input))

    _ = await io_task
    _ = await prog_task


if __name__ == '__main__':
    asyncio.run(solve())

