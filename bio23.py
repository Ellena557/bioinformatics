import numpy as np


def has_nums(st):
    res = any(ch.isdigit() for ch in st)
    return res


def get_blosum_scores():
    text = """    A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y 
    A  4  0 -2 -1 -2  0 -2 -1 -1 -1 -1 -2 -1 -1 -1  1  0  0 -3 -2
    C  0  9 -3 -4 -2 -3 -3 -1 -3 -1 -1 -3 -3 -3 -3 -1 -1 -1 -2 -2 
    D -2 -3  6  2 -3 -1 -1 -3 -1 -4 -3  1 -1  0 -2  0 -1 -3 -4 -3
    E -1 -4  2  5 -3 -2  0 -3  1 -3 -2  0 -1  2  0  0 -1 -2 -3 -2
    F -2 -2 -3 -3  6 -3 -1  0 -3  0  0 -3 -4 -3 -3 -2 -2 -1  1  3
    G  0 -3 -1 -2 -3  6 -2 -4 -2 -4 -3  0 -2 -2 -2  0 -2 -3 -2 -3
    H -2 -3 -1  0 -1 -2  8 -3 -1 -3 -2  1 -2  0  0 -1 -2 -3 -2  2
    I -1 -1 -3 -3  0 -4 -3  4 -3  2  1 -3 -3 -3 -3 -2 -1  3 -3 -1
    K -1 -3 -1  1 -3 -2 -1 -3  5 -2 -1  0 -1  1  2  0 -1 -2 -3 -2
    L -1 -1 -4 -3  0 -4 -3  2 -2  4  2 -3 -3 -2 -2 -2 -1  1 -2 -1
    M -1 -1 -3 -2  0 -3 -2  1 -1  2  5 -2 -2  0 -1 -1 -1  1 -1 -1
    N -2 -3  1  0 -3  0  1 -3  0 -3 -2  6 -2  0  0  1  0 -3 -4 -2
    P -1 -3 -1 -1 -4 -2 -2 -3 -1 -3 -2 -2  7 -1 -2 -1 -1 -2 -4 -3
    Q -1 -3  0  2 -3 -2  0 -3  1 -2  0  0 -1  5  1  0 -1 -2 -2 -1
    R -1 -3 -2  0 -3 -2  0 -3  2 -2 -1  0 -2  1  5 -1 -1 -3 -3 -2
    S  1 -1  0  0 -2  0 -1 -2  0 -2 -1  1 -1  0 -1  4  1 -2 -3 -2
    T  0 -1 -1 -1 -2 -2 -2 -1 -1 -1 -1  0 -1 -1 -1  1  5  0 -2 -2
    V  0 -1 -3 -2 -1 -3 -3  3 -2  1  1 -3 -2 -2 -3 -2  0  4 -3 -1
    W -3 -2 -4 -3  1 -2 -2 -3 -3 -2 -1 -4 -4 -2 -3 -3 -2 -3 11  2
    Y -2 -2 -3 -2  3 -3  2 -1 -2 -1 -1 -2 -3 -1 -2 -2 -2 -1  2  7 """

    alphabet = []

    # there are 20 different -> there will be 20 elements in the alphabet -> score_matrix will be 20 * 20
    score_matrix = np.zeros((20, 20))

    cur_symbol = ""
    num_alphs = 0
    counter = 0

    for symbol in text:
        if (num_alphs < 20) and (symbol != " "):
            alphabet.append(symbol)
            num_alphs += 1
        else:
            if (symbol == " "):
                if ((cur_symbol not in alphabet) and (has_nums(cur_symbol))):
                    score_matrix[int(counter // 20)][counter % 20] = int(cur_symbol)
                    counter += 1
                    cur_symbol = ""
            else:
                if ((symbol != "\n") and (symbol not in alphabet)):
                    cur_symbol += symbol

    #print(alphabet)
    #print(score_matrix)

    return alphabet, score_matrix


def get_cur_score(let1, let2, alphabet, score_matrix):
    id1 = alphabet.index(let1)
    id2 = alphabet.index(let2)
    res = score_matrix[id1][id2]
    return res


def do_global_alignment(st1, st2):
    sigma = 5
    alphabet, score_matrix = get_blosum_scores()
    n = len(st1)
    m = len(st2)
    res_matrix = np.zeros((n + 1, m + 1))

    from_what = np.zeros((n + 1, m + 1))
    # 1 - from up
    # 2 - from left
    # 3 - from diagonal

    for i in range(1, n + 1):
        res_matrix[i][0] = res_matrix[i - 1][0] - sigma
        from_what[i][0] = 1

    for j in range(1, m + 1):
        res_matrix[0][j] = res_matrix[0][j - 1] - sigma
        from_what[0][j] = 2

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            eq_variant = get_cur_score(st1[i - 1], st2[j - 1], alphabet, score_matrix) + res_matrix[i - 1][j - 1]
            all_variants = [
                res_matrix[i - 1][j] - sigma,
                res_matrix[i][j - 1] - sigma,
                eq_variant
            ]
            res_matrix[i][j] = np.max(all_variants)
            if (res_matrix[i][j] == eq_variant):
                from_what[i][j] = 3
            else:
                if (res_matrix[i][j] == res_matrix[i][j - 1] - sigma):
                    from_what[i][j] = 2
                else:
                    from_what[i][j] = 1

    res = res_matrix[n][m]

    cur_i = n
    cur_j = m
    pairs = []
    froms = []

    while (cur_i > 0 or cur_j > 0):
        pairs.append([cur_i, cur_j])
        if (from_what[cur_i][cur_j] == 3):
            cur_i -= 1
            cur_j -= 1
            froms.append(3)
        else:
            if (from_what[cur_i][cur_j] == 2):
                cur_j -= 1
                froms.append(2)
            else:
                cur_i -= 1
                froms.append(1)

    pairs = pairs[::-1]
    froms = froms[::-1]

    res_st1 = ""
    res_st2 = ""

    for elem in range(len(froms)):
        i, j = pairs[elem]
        f = froms[elem]
        if (f == 3):
            res_st1 += st1[i - 1]
            res_st2 += st2[j - 1]
        else:
            if (f == 2):
                res_st2 += st2[j - 1]
                res_st1 += "-"
            else:
                res_st2 += "-"
                res_st1 += st1[i - 1]

    return int(res), res_st1, res_st2


def main():
    st1 = input()
    st2 = input()
    res, res_st1, res_st2 = do_global_alignment(st1, st2)
    print(res)
    print(res_st1)
    print(res_st2)


if __name__ == '__main__':
    main()