import sys
import asyncio

from collections import defaultdict


def get_program():
    with open('input', 'rt') as f:
        intcode = [int(i.strip()) for i in f.read().strip().split(',')]

    intcode_dict = defaultdict(int)
    intcode_dict.update({index: code for index, code in enumerate(intcode)})

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


async def io(in_queue, out_queue, i, j):
    await in_queue.put(i)
    await in_queue.put(j)
    pulled = await out_queue.get()
    return pulled


async def solve():

    s = 0

    for i in range(0, 50):
        for j in range(0, 50):
            program = get_program()

            in_queue = asyncio.Queue()
            out_queue = asyncio.Queue()

            io_task = asyncio.create_task(io(in_queue, out_queue, i, j))
            prog_task = asyncio.create_task(run_program(program, in_queue, out_queue))

            pulled = await io_task
            _ = await prog_task

            if pulled:
                s += 1

            print('*' if pulled else ' ', end='')
        print()

    print('final', s)


if __name__ == '__main__':
    asyncio.run(solve())

