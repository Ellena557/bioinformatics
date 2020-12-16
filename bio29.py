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


def turn_genom_to_cycle(genom):
    black_edges = []
    nodes = []
    for chrom in genom:
        nodes = np.zeros(2 * len(chrom))
        for j in range(len(chrom)):
            i = chrom[j]
            if (i > 0):
                nodes[2 * j] = 2 * i - 1
                nodes[2 * j + 1] = 2 * i
                black_edges.append([2 * i - 1, 2 * i])
            else:
                nodes[2 * j] = (-2) * i
                nodes[2 * j + 1] = (-2) * i - 1
                black_edges.append([2 * abs(i), 2 * abs(i) - 1])
    return nodes, black_edges


def make_colored_edges(p):
    edges = []
    for chrom in p:
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
            if (edg[0] not in cur_els):
                cur_els.append(edg[0])
            if (edg[1] not in cur_els):
                cur_els.append(edg[1])
        p_cur = cycle_to_chrom(cur_els)
        p.append(p_cur)
    return p


def make_two_break(edges, two_break):
    res = []
    for i in range(len(edges)):
        res.append(edges[i])
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

    res[idx_1][0] = two_break[0]
    res[idx_1][1] = two_break[3]
    res[idx_2][1] = two_break[1]
    res[idx_2][0] = two_break[2]
    return res


def two_break_on_genome(p, two_break):
    black_edges = turn_genom_to_cycle(p)[1]
    colored_edges = make_colored_edges(p)

    all_edges = []
    for i in range(len(black_edges)):
        all_edges.append(black_edges[i])
    for j in range(len(colored_edges)):
        all_edges.append(colored_edges[j])

    all_new_edges = make_two_break(all_edges, two_break)
    pr = graph_to_genome(all_new_edges, black_edges)
    return pr


def print_in_appropriate_format(p):
    st_res = ""
    for res_i in p:
        st_res += "("
        for i in range(len(res_i)):
            if (res_i[i] > 0):
                st_res += "+"
            st_res += str(int(res_i[i]))
            st_res += " "
        st_res = st_res[:-1]
        st_res += ")"
    print(st_res)
    return st_res


def graph_has_cycles_notrivial(edges):
    res = 0
    rest_edges = []
    for i in range(len(edges)):
        rest_edges.append(edges[i])

    while (len(rest_edges) > 0):
        start_i = rest_edges[0][0]
        cur_i = rest_edges[0][1]
        cyc_len = 0
        rest_edges.remove([start_i, cur_i])
        while (cur_i != start_i):
            has_edge = 0
            for j in range(len(rest_edges)):
                if (rest_edges[j][0] == cur_i):
                    cur_i = rest_edges[j][1]
                    pair = rest_edges[j]
                    rest_edges.remove(pair)
                    has_edge = 1
                    cyc_len += 1
                    break
                if (rest_edges[j][1] == cur_i):
                    cur_i = rest_edges[j][0]
                    pair = rest_edges[j]
                    rest_edges.remove(pair)
                    has_edge = 1
                    cyc_len += 1
                    break
            if (has_edge == 0):
                break
        if (cur_i == start_i and cyc_len > 1):
            res = 1
    return res


def find_cycle(edges):
    # we assume that the graph definitely has a cycle
    rest_edges = []
    for i in range(len(edges)):
        rest_edges.append(edges[i])

    while (len(rest_edges) > 0):
        cycle = []
        start_i = rest_edges[0][0]
        cur_i = rest_edges[0][1]
        cyc_len = 0
        cycle.append([start_i, cur_i])
        rest_edges.remove([start_i, cur_i])
        used_verts = []
        used_verts.append(start_i)
        while (cur_i != start_i):
            used_verts.append(cur_i)
            for j in range(len(rest_edges)):
                if (rest_edges[j][0] == cur_i):
                    cur_i = rest_edges[j][1]
                    pair = rest_edges[j]
                    cycle.append(pair)
                    rest_edges.remove(pair)
                    cyc_len += 1
                    break

                else:
                    if (rest_edges[j][1] == cur_i):
                        cur_i = rest_edges[j][0]
                        pair = rest_edges[j]
                        cycle.append([rest_edges[j][1], rest_edges[j][0]])
                        rest_edges.remove(pair)
                        cyc_len += 1
                        break

        if (cyc_len > 1):
            return cycle

    return []


def find_shortest_transformation(p, q):
    print_in_appropriate_format(p)
    all_p_chain = []
    cur_p = []
    for i in range(len(p)):
        cur_p.append(p[i])

    red_edges = make_colored_edges(p)
    blue_edges = make_colored_edges(q)
    all_edges = []
    rest_blue_edges = []
    rest_red_edges = []
    all_p_chain.append(red_edges)

    for i in range(len(red_edges)):
        all_edges.append(red_edges[i])
        rest_red_edges.append(red_edges[i])
    for i in range(len(blue_edges)):
        all_edges.append(blue_edges[i])
        rest_blue_edges.append(blue_edges[i])

    while (graph_has_cycles_notrivial(all_edges) == 1):
        cycle = find_cycle(all_edges)
        first_edges = []
        ind_1 = 0
        if (cycle[0] not in rest_red_edges):
            ind_1 = 1

        first_edges.append(cycle[ind_1])
        if (ind_1 + 2 < len(cycle)):
            first_edges.append(cycle[ind_1 + 2])
        else:
            first_edges.append(cycle[-len(cycle) + ind_1 + 2])

        i_1 = first_edges[0][0]
        i_2 = first_edges[0][1]
        i_3 = first_edges[1][0]
        i_4 = first_edges[1][1]

        p_new = two_break_on_genome(cur_p, [i_1, i_2, i_3, i_4])
        cur_p = p_new

        if ([i_1, i_2] in rest_red_edges):
            rest_red_edges.remove([i_1, i_2])
            all_edges.remove([i_1, i_2])
        else:
            rest_red_edges.remove([i_2, i_1])
            all_edges.remove([i_2, i_1])

        if ([i_3, i_4] in rest_red_edges):
            rest_red_edges.remove([i_3, i_4])
            all_edges.remove([i_3, i_4])
        else:
            rest_red_edges.remove([i_4, i_3])
            all_edges.remove([i_4, i_3])

        rest_red_edges.append([i_1, i_4])
        rest_red_edges.append([i_2, i_3])

        print_in_appropriate_format(cur_p)

        all_edges.append([i_1, i_4])
        all_edges.append([i_2, i_3])


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

    find_shortest_transformation(elemns, elemns2)


if __name__ == '__main__':
    main()