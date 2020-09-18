import numpy as np


def find_hamming_dist(g1, g2):
    cur_sum = 0
    for i in range(len(g1)):
        if (g1[i] != g2[i]):
            cur_sum += 1
    return cur_sum


def find_approx_pattern_count(text, p, d):
    counter = 0
    for i in range(len(text) - len(p) + 1):
        p2 = []
        for j in range(len(p)):
            p2.append(text[i + j])
        if (find_hamming_dist(p, p2) <= d):
            counter += 1
    return counter


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


def freq_w_mismatch(text, k, d):
    patterns = []
    for i in range(4 ** k):
        patterns.append(NumberToPattern(i, k))
    cur_max = 0
    cur_max_pats = []
    for pat in patterns:
        num = find_approx_pattern_count(text, pat, d)
        if (num > cur_max):
            cur_max_pats = []
            cur_max = num
            cur_max_pats.append(pat)
        else:
            if (num == cur_max):
                cur_max_pats.append(pat)
    return cur_max_pats

def final_result_hw4(text, k, d):
    res = freq_w_mismatch(text, k, d)
    st = ""
    for i in range(len(res)):
        st += str(res[i])
        st += " "
    print(st)


def main():
    text = input()
    k = int(input())
    d = int(input())
    final_result_hw4(text, k, d)


if __name__ == '__main__':
    main()