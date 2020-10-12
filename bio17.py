import numpy as np


def find_num_peps(mass):
    all_mass = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

    # num_peps[i] = num of peptides with total mass = i
    num_peps = np.zeros(mass)

    #initial values: there is at least 1 peptide
    for j in range(len(all_mass)):
        n = all_mass[j]
        num_peps[n - 1] = 1

    for cur_mass in range(mass):
        for n in range(len(all_mass)):
            cur_n = all_mass[n]
            if (cur_mass >= cur_n):
                num_peps[cur_mass] += num_peps[cur_mass - cur_n]

    res = int(num_peps[-1])
    return res


def main():
    m = int(input())
    res = find_num_peps(m)
    print(res)


if __name__ == '__main__':
    main()