intcode = [1,0,0,0,99]   # --> 2,0,0,0,99
intcode = [2,3,0,3,99]   # --> 2,3,0,6,99
intcode = [2,4,4,5,99,0]  # --> 2,4,4,5,99,9801
intcode = [1,1,1,4,99,5,6,0,99]   # --> 30,1,1,4,2,5,6,0,99

intcode = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,2,19,13,23,1,23,10,27,1,13,27,31,2,31,10,35,1,35,9,39,1,39,13,43,1,13,43,47,1,47,13,51,1,13,51,55,1,5,55,59,2,10,59,63,1,9,63,67,1,6,67,71,2,71,13,75,2,75,13,79,1,79,9,83,2,83,10,87,1,9,87,91,1,6,91,95,1,95,10,99,1,99,13,103,1,13,103,107,2,13,107,111,1,111,9,115,2,115,10,119,1,119,5,123,1,123,2,127,1,127,5,0,99,2,14,0,0]

intcode[1] = 12
intcode[2] = 2

instruction_pointer = 0

while True:
    opcode = intcode[instruction_pointer]
    #print(instruction_pointer, opcode)

    if opcode == 1:
        a_ptr = intcode[instruction_pointer+1]
        b_ptr = intcode[instruction_pointer+2]
        c_ptr = intcode[instruction_pointer+3]

        result = intcode[a_ptr] + intcode[b_ptr]
        intcode[c_ptr] = result

        instruction_pointer += 4

    elif opcode == 2:
        a_ptr = intcode[instruction_pointer+1]
        b_ptr = intcode[instruction_pointer+2]
        c_ptr = intcode[instruction_pointer+3]

        result = intcode[a_ptr] * intcode[b_ptr]
        intcode[c_ptr] = result

        instruction_pointer += 4

    elif opcode == 99:
        break

    else:
        raise Exception('?')

print(intcode)

