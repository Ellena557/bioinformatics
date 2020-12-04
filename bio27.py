def find_num_breakpoints(elems):
    num_breaks = 0
    if (elems[0] != 1):
        num_breaks += 1
    if (elems[-1] != len(elems)):
        num_breaks += 1
    for k in range(len(elems) - 1):
        if (elems[k + 1] - elems[k] != 1):
            num_breaks += 1
    print(num_breaks)


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
    find_num_breakpoints(elemns)


if __name__ == '__main__':
    main()