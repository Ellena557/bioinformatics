import numpy as np


def turn_chromosome_to_cycle(chrom):
    nodes = np.zeros(2 * len(chrom))
    for j in range(len(chrom)):
        i = chrom[j]
        if (i > 0):
            nodes[2 * j] = 2 * i - 1
            nodes[2 * j + 1] = 2 * i
        else:
            nodes[2 * j] = (-2) * i
            nodes[2 * j + 1] =(-2) * i - 1
    return nodes


def make_colored_edges(p):
    edges = []
    for chrom in p:
        nodes = turn_chromosome_to_cycle(chrom)
        for j in range(len(chrom) - 1):
            edges.append([nodes[2 * j + 1], nodes[2 * j + 2]])
        last_j = 2 * len(chrom) - 1
        edges.append([nodes[last_j], nodes[0]])
    return edges


def find_num_cycles(edges):
    res = 0
    rest_edges = []
    for i in range(len(edges)):
        rest_edges.append(edges[i])

    while (len(rest_edges) > 0):
        start_i = rest_edges[0][0]
        cur_i = rest_edges[0][1]
        rest_edges.remove([start_i, cur_i])
        while (cur_i != start_i):
            for j in range(len(rest_edges)):
                if (rest_edges[j][0] == cur_i):
                    cur_i = rest_edges[j][1]
                    pair = rest_edges[j]
                    rest_edges.remove(pair)
                    break
                if (rest_edges[j][1] == cur_i):
                    cur_i = rest_edges[j][0]
                    pair = rest_edges[j]
                    rest_edges.remove(pair)
                    break
        res += 1

    return res


def find_break_dist(p, q):
    colored_edges_p = make_colored_edges(p)
    colored_edges_q = make_colored_edges(q)

    all_edges_pq = []
    all_edges_qq = []
    for i in range(len(colored_edges_p)):
        all_edges_pq.append(colored_edges_p[i])
    for i in range(len(colored_edges_q)):
        all_edges_pq.append(colored_edges_q[i])
        all_edges_qq.append(colored_edges_q[i])
        all_edges_qq.append(colored_edges_q[i])

    cycles_pq = find_num_cycles(all_edges_pq)
    blocks_pq = find_num_cycles(all_edges_qq)   #by theorem

    res = blocks_pq - cycles_pq
    return res


def main():
    st = input()
    st2 = input()
    elemns = []
    cur_elem = []
    cur = ''
    for i in range(1, len(st)):
        if (st[i] == " " or st[i] == ")"):
            cur_elem.append(int(cur))
            cur = ""
        else:
            cur += st[i]
        if (st[i] == ")"):
            elemns.append(cur_elem)
            cur_elem = []
        if (st[i] == "("):
            cur = ""

    elemns2 = []
    cur_elem = []
    cur = ''
    for i in range(1, len(st2)):
        if (st2[i] == " " or st2[i] == ")"):
            cur_elem.append(int(cur))
            cur = ""
        else:
            cur += st2[i]
        if (st2[i] == ")"):
            elemns2.append(cur_elem)
            cur_elem = []
        if (st2[i] == "("):
            cur = ""

    res = find_break_dist(elemns, elemns2)
    print(res)


if __name__ == '__main__':
    main()