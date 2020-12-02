def print_res(sort_parts, seq):
    res_arrays = int(len(sort_parts) / len(seq))
    for i in range(res_arrays):
        cur = "("
        for j in range(len(seq)):
            elem = sort_parts[i * len(seq) + j]
            if (int(elem) < 0):
                cur += str(elem)
                cur += " "
            else:
                cur += "+"
                cur += str(elem)
                cur += " "
        cur = cur[:-1]
        cur += ")"
        print(cur)


def do_greedy_sort(seq):
    sort_pats = []
    cur_seq = []
    for k in range(len(seq)):
        cur_seq.append(seq[k])
    #sort_pats.append(cur_seq)
    for k in range(len(seq)):
        if (abs(cur_seq[k]) != (k + 1)):
            for j in range(k, len(seq)):
                if (abs(cur_seq[j]) == (k + 1)):
                    t = cur_seq[j]
                    cur_seq[j] = - cur_seq[k]
                    cur_seq[k] = - t
                    for tt in range(k + 1, j):
                        cur_seq[tt] *= (-1)
                    if (j - k >= 2):
                        cur_seq[k + 1:j] = cur_seq[k + 1 : j][::-1]
            for t in cur_seq:
                sort_pats.append(t)
        if (cur_seq[k] == -(k + 1)):
            cur_seq[k] = k+1
            for t in cur_seq:
                sort_pats.append(t)

    print_res(sort_pats, seq)


def main():
    st = input()
    elemns = []
    cur = ''
    for i in range(1, len(st)):
        if (st[i] == " " or st[i] == ")"):
            elemns.append(int(cur))
            cur = ""
        else:
            cur += st[i]
    do_greedy_sort(elemns)


if __name__ == '__main__':
    main()