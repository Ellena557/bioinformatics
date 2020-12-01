import numpy as np


def do_multiple_alignment(st1, st2, st3):
    n = len(st1)
    m = len(st2)
    l = len(st3)
    s_vals = np.zeros((n + 1, m + 1, l + 1))
    from_what = np.zeros((n + 1, m + 1, l + 1))
    # i : 1
    # j : 2
    # k : 3
    # i,j,k : 4

    #goods_i = array of indexes of i-th string which elements are in a common string
    goods1 = []
    goods2 = []
    goods3 = []

    for i in range(1, m + 1):
        for k in range(1, l + 1):
            s_vals[0][i][k] = 0
            from_what[0][i][k] = 1

    for i in range(1, n + 1):
        for k in range(1, l + 1):
            s_vals[i][0][k] = 0
            from_what[i][0][k] = 2

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            s_vals[i][j][0] = 0
            from_what[i][j][0] = 3

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            for k in range(1, l + 1):
                eq_val = 0
                if (st1[i - 1] == st2[j - 1] and st2[j - 1] == st3[k - 1]):
                    s_vals[i][j][k] = s_vals[i-1][j-1][k-1] + 1
                    from_what[i][j][k] = 4
                else:
                    vals = [
                        s_vals[i][j][k - 1],
                        s_vals[i][j - 1][k],
                        s_vals[i - 1][j][k],
                        eq_val
                    ]
                    s_vals[i][j][k] = np.max(vals)
                    if (s_vals[i][j][k] == s_vals[i - 1][j][k]):
                        from_what[i][j][k] = 1
                    else:
                        if (s_vals[i][j][k] == s_vals[i][j - 1][k]):
                            from_what[i][j][k] = 2
                        else:
                            from_what[i][j][k] = 3

    result = s_vals[n][m][k]

    cur_i = n
    cur_j = m
    cur_k = l
    pairs = []
    froms = []

    while ((cur_i > 0 or cur_j > 0) or cur_k > 0):
        pairs.append([cur_i, cur_j, cur_k])
        if (from_what[cur_i][cur_j][cur_k] == 4):
            cur_i -= 1
            cur_j -= 1
            cur_k -= 1
            froms.append(4)
        else:
            if (from_what[cur_i][cur_j][cur_k] == 3 and cur_k > 0):
                cur_k -= 1
                froms.append(3)
            else:
                if (from_what[cur_i][cur_j][cur_k] == 2 and cur_j > 0):
                    cur_j -= 1
                    froms.append(2)
                else:
                    if (from_what[cur_i][cur_j][cur_k] == 1 and cur_i > 0):
                        cur_i -= 1
                        froms.append(1)
                    else:
                        break

    pairs = pairs[::-1]
    froms = froms[::-1]

    for elem in range(len(froms)):
        i, j, k = pairs[elem]
        f = froms[elem]
        if (f == 4):
            goods1.append(i)
            goods2.append(j)
            goods3.append(k)

    res_st1 = ""
    res_st2 = ""
    res_st3 = ""

    good_idx_g = [
        goods1[0],
        goods2[0],
        goods3[0]
    ]
    good_id_curr = np.max(good_idx_g)
    prev_goods = [-1, -1, -1]
    cur_i = 0
    cur_j = 0
    cur_k = 0

    for g in range(len(goods1)):
        if (g > 0):
            good_idx_g = [
                goods1[g] - goods1[g - 1],
                goods2[g] - goods2[g - 1],
                goods3[g] - goods3[g - 1]
            ]
            good_id_curr = np.max(good_idx_g)
            prev_goods = [
                goods1[g - 1] - 1,
                goods2[g - 1] - 1,
                goods3[g - 1] - 1
            ]

        for i in range(good_id_curr - good_idx_g[0]):
            res_st1 += '-'

        if (g == 0):
            res_st1 += st1[cur_i]
            cur_i += 1
        for i in range(good_idx_g[0]):
            res_st1 += st1[cur_i]
            cur_i += 1

        for i in range(good_id_curr - good_idx_g[1]):
            res_st2 += '-'

        if (g == 0):
            res_st2 += st2[cur_j]
            cur_j += 1

        for i in range(good_idx_g[1]):
            res_st2 += st2[cur_j]
            cur_j += 1

        for i in range(good_id_curr - good_idx_g[2]):
            res_st3 += '-'

        if (g == 0):
            res_st3 += st3[cur_k]
            cur_k += 1

        for i in range(good_idx_g[2]):
            res_st3 += st3[cur_k]
            cur_k += 1

    rest_symbs = [
        n - cur_i,
        m - cur_j,
        l - cur_k
    ]

    max_rest = np.max(rest_symbs)

    for i in range(rest_symbs[0]):
        res_st1 += st1[cur_i]
        cur_i += 1

    for i in range(max_rest - rest_symbs[0]):
        res_st1 += "-"

    for i in range(rest_symbs[1]):
        res_st2 += st2[cur_j]
        cur_j += 1

    for i in range(max_rest - rest_symbs[1]):
        res_st2 += "-"

    for i in range(rest_symbs[2]):
        res_st3 += st3[cur_k]
        cur_k += 1

    for i in range(max_rest - rest_symbs[2]):
        res_st3 += "-"

    return int(result), res_st1, res_st2, res_st3


def main():
    st1 = input()
    st2 = input()
    st3 = input()
    res, res_st1, res_st2, res_st3 = do_multiple_alignment(st1, st2, st3)
    print(res)
    print(res_st1)
    print(res_st2)
    print(res_st3)


if __name__ == '__main__':
    main()