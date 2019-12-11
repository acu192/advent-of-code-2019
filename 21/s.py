import asyncio

from collections import defaultdict


def get_program():
    intcode = [3,8,1005,8,334,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,28,2,1108,5,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,55,1,102,18,10,1,2,5,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,84,1,106,11,10,2,1008,6,10,1,4,4,10,1006,0,55,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,102,1,8,121,1,107,9,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,147,2,1002,4,10,2,104,18,10,1,107,16,10,1,108,8,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,185,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,208,2,1009,16,10,1006,0,7,1006,0,18,1,1105,8,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,243,2,1105,20,10,2,106,10,10,1006,0,67,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,276,2,1103,5,10,2,1104,7,10,1006,0,35,2,1105,3,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1002,8,1,314,101,1,9,9,1007,9,1097,10,1005,10,15,99,109,656,104,0,104,1,21102,936995824532,1,1,21101,0,351,0,1105,1,455,21102,1,387508445964,1,21102,362,1,0,1106,0,455,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,235244973059,1,21101,409,0,0,1106,0,455,21102,179410541659,1,1,21101,0,420,0,1105,1,455,3,10,104,0,104,0,3,10,104,0,104,0,21101,868402070292,0,1,21102,1,443,0,1106,0,455,21102,1,709584749324,1,21102,454,1,0,1106,0,455,99,109,2,22102,1,-1,1,21101,40,0,2,21102,486,1,3,21101,0,476,0,1106,0,519,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,481,482,497,4,0,1001,481,1,481,108,4,481,10,1006,10,513,1101,0,0,481,109,-2,2106,0,0,0,109,4,2102,1,-1,518,1207,-3,0,10,1006,10,536,21102,0,1,-3,21202,-3,1,1,22102,1,-2,2,21102,1,1,3,21102,555,1,0,1106,0,560,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,583,2207,-4,-2,10,1006,10,583,21201,-4,0,-4,1106,0,651,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21102,602,1,0,1106,0,560,22102,1,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,621,21102,0,1,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,643,21201,-1,0,1,21102,643,1,0,106,0,518,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]

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


def update_direction(d, x, y, turn):
    if d == 0:  # up
        if turn == 0:  # left
            return 3, x-1, y
        else:          # right
            return 1, x+1, y

    elif d == 1:  # right
        if turn == 0:  # left
            return 0, x, y-1
        else:          # right
            return 2, x, y+1

    elif d == 2:  # down
        if turn == 0:  # left
            return 1, x+1, y
        else:          # right
            return 3, x-1, y

    elif d == 3:  # left
        if turn == 0:  # left
            return 2, x, y+1
        else:          # right
            return 0, x, y-1


async def io(in_queue, out_queue):
    d = 0   # direction: 0 = up, 1 = right, 2 = down, 3 = left
    x, y = 0, 0
    colors = defaultdict(int)   # black by default; 0 = black    1 = white

    painted = set()

    while True:
        await in_queue.put(colors[(x, y)])

        paint = await out_queue.get()
        if paint is None:
            return len(painted)
        colors[(x, y)] = paint
        painted.add((x, y))

        turn = await out_queue.get()
        if turn is None:
            return len(painted)
        d, x, y = update_direction(d, x, y, turn)


async def solve():

    program = get_program()
    in_queue = asyncio.Queue()
    out_queue = asyncio.Queue()

    task = asyncio.create_task(io(in_queue, out_queue))

    await run_program(program, in_queue, out_queue)

    answer = await task

    print(answer)


if __name__ == '__main__':
    asyncio.run(solve())

