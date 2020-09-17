import numpy as np

def lexic_order(p):
    if (p == 'A'):
        return 0
    else:
        if (p == 'T'):
            return 3
        else:
            if (p == 'C'):
                return 1
            else:
                return 2


def PatternToNumber(pat, k):
    n_letters = len(pat)
    num = 0
    for i in range(n_letters):
        num += 4 ** (n_letters - i - 1) * lexic_order(pat[i])
    return num


def rev_lexic_order(p):
    if (p == 0):
        return "A"
    else:
        if (p == 3):
            return "T"
        else:
            if (p == 1):
                return "C"
            else:
                return "G"


def NumberToPattern(num, k):
    pat = ""
    n = num
    for i in range(k):
        let = n % 4
        n = n // 4
        pat += rev_lexic_order(let)
    return pat[::-1]


def ClumpFindingFast(genom, k, L, t):
    res_clumps = []
    is_clump = np.zeros(4 ** k)

    for i in range(len(genom) - L + 1):
        counts = np.zeros(4 ** k)
        for j in range(0, L - k):
            pat = genom[i + j : i + j + k]
            num = PatternToNumber(pat, k)
            counts[num] += 1
            if (counts[num] >= t):
                is_clump[num] = 1

    for d in range(4 ** k):
        if (is_clump[d] == 1):
            #print(counts[d])
            res_clumps.append(NumberToPattern(d, k))
    return res_clumps

def final_result_hw1(gen, k, L, t):
    res = ClumpFindingFast(gen, k, L, t)
    str = ""
    for i in range(len(res)):
        str += res[i]
        str += " "
    print(str)

def main():
    genome = input()
    k = int(input())
    L = int(input())
    t = int(input())
    final_result_hw1(genome, k, L, t)

if __name__ == '__main__':
    main()