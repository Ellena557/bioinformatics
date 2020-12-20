import numpy as np


def turn_chromosome_to_cycle(chrom):
    black_edges = []
    nodes = np.zeros(2 * len(chrom))
    for j in range(len(chrom)):
        i = chrom[j]
        if (i > 0):
            nodes[2 * j] = 2 * i - 1
            nodes[2 * j + 1] = 2 * i
            black_edges.append([2 * i - 1, 2 * i])
        else:
            nodes[2 * j] = (-2) * i
            nodes[2 * j + 1] =(-2) * i - 1
            black_edges.append([2 * abs(i), 2 * abs(i) - 1])
    return nodes, black_edges


def make_colored_edges(chrom):
    edges = []
    #for chrom in p:
    #cycle_edges = []
    nodes = turn_chromosome_to_cycle(chrom)[0]
    for j in range(len(chrom) - 1):
        edges.append([nodes[2 * j + 1], nodes[2 * j + 2]])
    last_j = 2 * len(chrom) - 1
    edges.append([nodes[last_j], nodes[0]])
    return edges


def cycle_to_chrom(nodes):
    chrom = np.zeros(int(len(nodes) / 2))
    for j in range(int(len(nodes) / 2)):
        if (nodes[2 * j] < nodes[2 * j + 1]):
            chrom[j] = nodes[2 * j + 1] / 2
        else:
            chrom[j] = - nodes[2 * j] / 2
    return chrom


def graph_to_genome(graph, black_edges):
    p = []
    cur_chrom = []
    all_chroms = []
    rest_edges = []
    for i in range(len(graph)):
        rest_edges.append(graph[i])
    rest_black_edges = []
    for i in range(len(black_edges)):
        rest_black_edges.append(black_edges[i])

    while(len(rest_edges) > 0):
        start_i = rest_black_edges[0][0]
        cur_i = rest_black_edges[0][1]
        cur_chrom.append([start_i, cur_i])
        rest_black_edges.remove([start_i, cur_i])
        rest_edges.remove([start_i, cur_i])
        while(cur_i != start_i):
            for j in range(len(rest_edges)):
                if (rest_edges[j][0] == cur_i):
                    cur_i = rest_edges[j][1]
                    cur_chrom.append(rest_edges[j])
                    if (rest_edges[j] in rest_black_edges):
                        rest_black_edges.remove(rest_edges[j])
                    pair = rest_edges[j]
                    rest_edges.remove(pair)
                    break
                if (rest_edges[j][1] == cur_i):
                    cur_i = rest_edges[j][0]
                    cur_chrom.append(rest_edges[j])
                    if (rest_edges[j] in rest_black_edges):
                        rest_black_edges.remove(rest_edges[j])
                    pair = rest_edges[j]
                    rest_edges.remove(pair)
                    break

        all_chroms.append(cur_chrom)
        cur_chrom = []

    for chr in all_chroms:
        cur_els = []
        for edg in chr:
            cur_els.append(edg[0])
        p_cur = cycle_to_chrom(cur_els)
        p.append(p_cur)
    return p


def make_two_break(edges, two_break):
    res = edges
    idx_1 = -1

    if ([two_break[0], two_break[1]] in edges):
        idx_1 = edges.index([two_break[0], two_break[1]])
    else:
        idx_1 = edges.index([two_break[1], two_break[0]])

    idx_2 = -1
    if ([two_break[2], two_break[3]] in edges):
        idx_2 = edges.index([two_break[2], two_break[3]])
    else:
        idx_2 = edges.index([two_break[3], two_break[2]])

    pair_1 = edges[idx_1]
    pair_2 = edges[idx_2]
    pos_1 = pair_1.index(two_break[1])
    pos_2 = pair_2.index(two_break[2])
    res[idx_1][pos_1] = two_break[2]
    res[idx_2][pos_2] = two_break[1]

    return res


def two_break_on_genome(p, two_break):
    black_edges = turn_chromosome_to_cycle(p)[1]
    colored_edges = make_colored_edges(p)
    all_edges = []
    for i in range(len(black_edges)):
        all_edges.append(black_edges[i])
    for j in range(len(colored_edges)):
        all_edges.append(colored_edges[j])
    all_new_edges = make_two_break(all_edges, two_break)
    pr = graph_to_genome(all_new_edges, black_edges)
    return pr


def main():
    st = input()
    breaks = input()
    elemns = []
    cur = ''
    for i in range(len(st)):
        if ((st[i] == " " or st[i] == ")") or (st[i] == ",")):
            if (len(cur) > 0):
                elemns.append(int(cur))
                cur = ""
        else:
            if (st[i] != "("):
                cur += st[i]

    two_breaks = []
    cur = ""
    for i in range(len(breaks)):
        if (breaks[i] == " " or breaks[i] == ","):
            if (len(cur) > 0):
                two_breaks.append(int(cur))
                cur = ""
        else:
            cur += breaks[i]

    res = two_break_on_genome(elemns, two_breaks)
    st_res = ""
    for res_i in res:
        st_res += "("
        for i in range(len(res_i)):
            if (res_i[i] > 0):
                st_res += "+"
            st_res += str(int(res_i[i]))
            st_res += " "
        st_res = st_res[:-1]
        st_res += ")"
    print(st_res)


if __name__ == '__main__':
    main()