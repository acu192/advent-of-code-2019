with open('input', 'rt') as f:
    digits = list(f.read().strip())

size = 25 * 6

def num_stuff(c, thing):
    a = 0
    for i in c:
        if i == thing:
            a += 1
    return a

min_z = size + 1

for i in range(0, len(digits), size):
    chunk = digits[i:i+size]
    zeros = num_stuff(chunk, '0')
    if zeros < min_z:
        min_chunk = chunk
        min_z = zeros

print(num_stuff(min_chunk, '1') * num_stuff(min_chunk, '2'))

