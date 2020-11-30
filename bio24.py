import numpy as np


def has_nums(st):
    res = any(ch.isdigit() for ch in st)
    return res


def get_pam_scores():
    text = """   A  C  D  E  F  G  H  I  K  L  M  N  P  Q  R  S  T  V  W  Y
    A  2 -2  0  0 -3  1 -1 -1 -1 -2 -1  0  1  0 -2  1  1  0 -6 -3
    C -2 12 -5 -5 -4 -3 -3 -2 -5 -6 -5 -4 -3 -5 -4  0 -2 -2 -8  0
    D  0 -5  4  3 -6  1  1 -2  0 -4 -3  2 -1  2 -1  0  0 -2 -7 -4
    E  0 -5  3  4 -5  0  1 -2  0 -3 -2  1 -1  2 -1  0  0 -2 -7 -4
    F -3 -4 -6 -5  9 -5 -2  1 -5  2  0 -3 -5 -5 -4 -3 -3 -1  0  7
    G  1 -3  1  0 -5  5 -2 -3 -2 -4 -3  0  0 -1 -3  1  0 -1 -7 -5
    H -1 -3  1  1 -2 -2  6 -2  0 -2 -2  2  0  3  2 -1 -1 -2 -3  0
    I -1 -2 -2 -2  1 -3 -2  5 -2  2  2 -2 -2 -2 -2 -1  0  4 -5 -1
    K -1 -5  0  0 -5 -2  0 -2  5 -3  0  1 -1  1  3  0  0 -2 -3 -4
    L -2 -6 -4 -3  2 -4 -2  2 -3  6  4 -3 -3 -2 -3 -3 -2  2 -2 -1
    M -1 -5 -3 -2  0 -3 -2  2  0  4  6 -2 -2 -1  0 -2 -1  2 -4 -2
    N  0 -4  2  1 -3  0  2 -2  1 -3 -2  2  0  1  0  1  0 -2 -4 -2
    P  1 -3 -1 -1 -5  0  0 -2 -1 -3 -2  0  6  0  0  1  0 -1 -6 -5
    Q  0 -5  2  2 -5 -1  3 -2  1 -2 -1  1  0  4  1 -1 -1 -2 -5 -4
    R -2 -4 -1 -1 -4 -3  2 -2  3 -3  0  0  0  1  6  0 -1 -2  2 -4
    S  1  0  0  0 -3  1 -1 -1  0 -3 -2  1  1 -1  0  2  1 -1 -2 -3
    T  1 -2  0  0 -3  0 -1  0  0 -2 -1  0  0 -1 -1  1  3  0 -5 -3
    V  0 -2 -2 -2 -1 -1 -2  4 -2  2  2 -2 -1 -2 -2 -1  0  4 -6 -2
    W -6 -8 -7 -7  0 -7 -3 -5 -3 -2 -4 -4 -6 -5  2 -2 -5 -6 17  0
    Y -3  0 -4 -4  7 -5  0 -1 -4 -1 -2 -2 -5 -4 -4 -3 -3 -2  0 10 """

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

    return alphabet, score_matrix


def get_cur_score(let1, let2, alphabet, score_matrix):
    id1 = alphabet.index(let1)
    id2 = alphabet.index(let2)
    res = score_matrix[id1][id2]
    return res


def do_local_alignment(st1, st2):
    sigma = 5
    alphabet, score_matrix = get_pam_scores()
    n = len(st1)
    m = len(st2)
    res_matrix = np.zeros((n + 1, m + 1))

    from_what = np.zeros((n + 1, m + 1))
    # 1 - from up
    # 2 - from left
    # 3 - from diagonal
    # 4 - from (0, 0) OR right to (n, m)

    for i in range(1, n + 1):
        res_matrix[i][0] = res_matrix[i - 1][0] - sigma
        from_what[i][0] = 1

        # add an edge to (0,0)
        if (res_matrix[i][0] < 0):
            res_matrix[i][0] = 0
            from_what[i][0] = 4

    for j in range(1, m + 1):
        res_matrix[0][j] = res_matrix[0][j - 1] - sigma
        from_what[0][j] = 2

        # add an edge to (0,0)
        if (res_matrix[0][j] < 0):
            res_matrix[0][j] = 0
            from_what[0][j] = 4

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

            # add "edge" to (0, 0)
            if(res_matrix[i][j] < 0):
                res_matrix[i][j] = 0
                from_what[i][j] = 4

    res = res_matrix[n][m]
    from_edge = []

    # go straight to the end
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # not the last element
            if (i + j < n + m):
                if (res_matrix[i][j] > res):
                    res = res_matrix[i][j]
                    from_what[n][m] = 4
                    from_edge = [i, j]
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
                if (from_what[cur_i][cur_j] == 1):
                    cur_i -= 1
                    froms.append(1)
                else:
                    if (cur_i == n and cur_j == m):
                        froms.append(4)
                        cur_i = from_edge[0]
                        cur_j = from_edge[1]
                    else:
                        froms.append(4)
                        cur_i = 0
                        cur_j = 0

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
                if (f == 1):
                    res_st2 += "-"
                    res_st1 += st1[i - 1]
                # in case of f == 4 we do nothing
    return int(res), res_st1, res_st2


def main():
    st1 = input()
    st2 = input()
    res, res_st1, res_st2 = do_local_alignment(st1, st2)
    print(res)
    print(res_st1)
    print(res_st2)


if __name__ == '__main__':
    main()