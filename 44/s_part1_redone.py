from collections import defaultdict
from itertools import count


steps = []


with open('../43/input', 'rt') as f:
    for line in f:
        line = line.strip()
        params = line.split(' ')
        if line.startswith('cut'):
            steps.append(('cut', int(params[-1])))
        elif line.startswith('deal into'):
            steps.append(('reverse', None))
        elif line.startswith('deal with'):
            steps.append(('inc', int(params[-1])))
        else:
            assert False


def egcd(a, b):
    # See: https://discuss.codechef.com/t/a-tutorial-on-the-extended-euclids-algorithm/2923
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


modinv_cache = {}


def modinv(a, m):
    # See: https://discuss.codechef.com/t/a-tutorial-on-the-extended-euclids-algorithm/2923
    if (a, m) in modinv_cache:
        return modinv_cache[(a, m)]
    g, x, y = egcd(a, m)
    if g != 1:
        solution = None  # modular inverse does not exist
    else:
        solution = x % m
    modinv_cache[(a, m)] = solution
    return solution


def get_card(interst, lenth, shuffle_steps):
    for step, n in reversed(shuffle_steps):
        if step == 'cut':
            if n < 0:
                n = lenth + n
            n = lenth - n
            interst = (lenth + interst - n) % lenth

        elif step == 'reverse':
            interst = lenth - interst - 1

        elif step == 'inc':
            inv = modinv(n, lenth)
            interst = (interst * inv) % lenth

    return interst


if __name__ == '__main__':

    lenth = 10007

    # This implementation needs no significant memory, which is cool!
    # (This is in contrast to my solution on part 1, as you know.)

    for i in range(lenth):
        c = get_card(i, lenth, steps)
        if c == 2019:
            print(i)
            break

