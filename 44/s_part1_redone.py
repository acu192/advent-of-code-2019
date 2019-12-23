from s import get_card, steps


if __name__ == '__main__':

    lenth = 10007

    # This implementation needs no significant memory, which is cool!
    # (This is in contrast to my solution on part 1, as you know.)

    for i in range(lenth):
        c = get_card(i, lenth, steps)
        if c == 2019:
            print(i)
            break

