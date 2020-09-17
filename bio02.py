import numpy as np


def add_num(p):
    if (p == 'A'):
        return 0
    else:
        if (p == 'T'):
            return 0
        else:
            if (p == 'C'):
                return -1
            else:
                return 1


def find_min_skew(g):
    skew = np.zeros(len(g) + 1)
    cur_min = 0
    for i in range(len(g)):
        skew[i + 1] = skew[i] + add_num(g[i])
        if (skew[i + 1] < cur_min):
            cur_min = skew[i + 1]

    all_min_ids = []
    for i in range(len(g)):
        if (skew[i + 1] == cur_min):
            all_min_ids.append(i + 1)

    return all_min_ids


def final_result_hw2(gen):
    res = find_min_skew(gen)
    st = ""
    for i in range(len(res)):
        st += str(res[i])
        st += " "
    print(st)


def main():
    genome = input()
    final_result_hw2(genome)


if __name__ == '__main__':
    main()