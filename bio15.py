import numpy as np


def compine_genom_from_path(path, d, k):
    res = ""
    extra_res = ""

    for i in range(len(path)):
        res += path[i][0][0]
        if (i == 0):
            extra_res += path[0][1]
        else:
            extra_res += path[i][1][-1]
    res += path[len(path) - 1][0][1:]
    res += extra_res[-d - k:]
    return res


def do_str_reconstruction(k, d, text):
    res = compine_genom_from_path(text, d, k)
    return res


def final_result_hw15(k, d, text):
    dna = []
    for i in range(len(text)):
        dna_cur = text[i]
        dna.append([dna_cur[:k], dna_cur[k + 1:]])

    res = do_str_reconstruction(k, d, dna)
    print(res)


def main():
    k = int(input())
    d = int(input())
    inext = 1
    text = []
    while (inext == 1):
        t = input()
        if (t == "-1"):  # it's a signal that is is the end of the text!
            inext = 0
        else:
            text.append(t)
    final_result_hw15(k, d, text)


if __name__ == '__main__':
    main()