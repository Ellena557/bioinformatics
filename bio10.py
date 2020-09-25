import numpy as np


def find_hamming_dist(g1, g2):
    cur_sum = 0
    for i in range(len(g1)):
        if (g1[i] != g2[i]):
            cur_sum += 1
    return cur_sum


def find_d_st(pat, st):
    ham = len(pat)
    for j in range(len(st) - len(pat) + 1):
        pat2 = []
        for i in range(len(pat)):
            pat2.append(st[i + j])
        ham2 = find_hamming_dist(pat, pat2)
        if (ham > ham2):
            ham = ham2
    return ham


def find_distance_between_pattern_and_strings(pat, dna):
    d = 0
    for st in dna:
        d += find_d_st(pat, st)
    return d


def final_result_hw10(pat, text):
    dna = []
    cur_dna = ""
    for j in range(len(text)):
        if (text[j] != " "):
            cur_dna += text[j]
        else:
            dna.append(cur_dna)
            cur_dna = ""
    dna.append(cur_dna)
    res = find_distance_between_pattern_and_strings(pat, dna)
    print(res)


def main():
    pat = input()
    text = input()
    final_result_hw10(pat, text)


if __name__ == '__main__':
    main()