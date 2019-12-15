import asyncio

from collections import defaultdict


def get_program():
    with open('../29/input', 'rt') as f:
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


async def go(direction, in_queue, out_queue):
    await in_queue.put(direction)

    while True:
        status = await out_queue.get()
        if status != 'input':
            break

    return status


def nextpos(direction, x, y):
    if direction == 1:
        return x+0, y+-1
    elif direction == 2:
        return x+0, y+1
    elif direction == 3:
        return x+-1, y+0
    else:
        return x+1, y+0


def reversedir(direction):
    if direction == 1:
        return 2
    elif direction == 2:
        return 1
    elif direction == 3:
        return 4
    else:
        return 3


async def step_once(direction, x, y, ship, curr_dist, in_queue, out_queue):
    next_x, next_y = nextpos(direction, x, y)

    if (next_x, next_y) in ship:
        next_status, next_dist = ship[(next_x, next_y)]
        if next_status == 0:  # wall
            return
        if next_dist <= curr_dist + 1:
            return    # we already found a shorter or equal-length path

    status = await go(direction, in_queue, out_queue)

    location = None   # OXYGEN LOCATION (if found)

    if status == 0:  # wall
        ship[(next_x, next_y)] = (0, curr_dist+1)
        return

    if status in (1, 2):  # open
        print('Stepped to', next_x, next_y)
        ship[(next_x, next_y)] = (1, curr_dist+1)
        if status == 2:
            location = (next_x, next_y)   # OXYGEN LOCATION IS FOUND
        for next_direction in (1, 2, 3, 4):
            ret = await step_once(next_direction, next_x, next_y, ship, curr_dist+1, in_queue, out_queue)
            if ret is not None:
                location = ret   # PROPOGATE ANSWER

    print('Stepping back...')
    await go(reversedir(direction), in_queue, out_queue)   # keep state consistence
    return location


async def io(in_queue, out_queue):
    ship = {}

    x, y = 0, 0

    ship[(x, y)] = (1, 0)  # status, dist

    location = None

    for direction in (1, 2, 3, 4):
        ret = await step_once(direction, x, y, ship, 0, in_queue, out_queue)
        if ret is not None:
            location = ret

    print('OXYGEN LOCATION', location)

    ship[location] = (2, None)   # dist doesn't matter anymore

    total = fill(ship)

    print('MINUTES TAKEN', total)


import itertools


def fill(ship):
    for i in itertools.count(1):
        something = False
        n_oxg = 0
        for (x, y), (status, _) in ship.copy().items():
            if status == 2:
                n_oxg += 1
                if ship[(x+1, y)][0] == 1:
                    ship[(x+1, y)] = (2, None)   # propogate the oxygen
                    something = True

                if ship[(x-1, y)][0] == 1:
                    ship[(x-1, y)] = (2, None)   # propogate the oxygen
                    something = True

                if ship[(x, y+1)][0] == 1:
                    ship[(x, y+1)] = (2, None)   # propogate the oxygen
                    something = True

                if ship[(x, y-1)][0] == 1:
                    ship[(x, y-1)] = (2, None)   # propogate the oxygen
                    something = True

        if not something:
            break

    return i-1  # the last iteration did nothing


async def solve():

    program = get_program()

    in_queue = asyncio.Queue()
    out_queue = asyncio.Queue()

    io_task = asyncio.create_task(io(in_queue, out_queue))
    prog_task = asyncio.create_task(run_program(program, in_queue, out_queue))

    _ = await io_task
    _ = await prog_task


if __name__ == '__main__':
    asyncio.run(solve())

