import numpy as np


def compine_genom_from_path(path):
    res = ""
    for i in range(len(path)):
        res += path[i][0]
    k = len(path[0])
    res += path[len(path) - 1][1:]
    return res


def find_euler_cycle(graph):
    # the form of a graph here will be definitely a euler graph -> no need for extra check
    edges = graph[1]
    verts = graph[0]
    degrees = np.zeros(len(verts))
    idx_of_start_vtx = 0

    for i in range(len(verts)):
        for j in range(len(verts)):
            degrees[i] += edges[i][j]
            degrees[j] -= edges[i][j]

    cycle_ids = []
    cur_cycle_ids = []
    not_visited_verts = []
    not_visited_verts.append(idx_of_start_vtx)

    while (1 == 1):
        cur_vert = idx_of_start_vtx
        cur_subcycle = []
        cur_subcycle.append(cur_vert)

        while (np.sum(edges[cur_vert]) > 0):
            first_vert = 1
            for j in range(len(verts)):
                if (edges[cur_vert][j] > 0 and first_vert == 1):
                    first_vert = 0
                    cur_subcycle.append(j)
                    edges[cur_vert][j] -= 1
                    cur_vert = j

        cur_cycle_ids = cur_subcycle + cur_cycle_ids

        is_visit = 1
        for t in range(len(cur_cycle_ids)):
            if (np.sum(edges[cur_cycle_ids[t]]) == 0):
                cycle_ids.append(cur_cycle_ids[t])
            else:
                idx_of_start_vtx = cur_cycle_ids[t]
                cur_cycle_ids = cur_cycle_ids[t + 1:]
                is_visit = 0
                break
        if (is_visit == 1):
            break

    #print(cycle_ids)
    res_pats = []
    for i in range(len(cycle_ids)):
        res_pats.append(verts[cycle_ids[i]])
    return res_pats


def make_db_graph(pats):
    vertices = []
    all_edges = np.zeros((2 * len(pats), 2 * len(pats)))
    for pat in pats:
        cur_pref = pat[:-1]
        cur_suf = pat[1:]
        if (cur_pref in vertices):
            idx_pref = vertices.index(cur_pref)
        else:
            idx_pref = len(vertices)
            vertices.append(cur_pref)
        if (cur_suf in vertices):
            idx_suf = vertices.index(cur_suf)
        else:
            idx_suf = len(vertices)
            vertices.append(cur_suf)
        all_edges[idx_pref][idx_suf] += 1
    return vertices, all_edges


def do_str_reconstruction(k, text):
    db_graph = make_db_graph(text)
    eul_path = find_euler_cycle(db_graph)
    res = compine_genom_from_path(eul_path)
    return res


def turn_to_2_sys(num, n):
    cur_num = num
    res = ""
    for i in range(n):
        res += str(cur_num % 2)
        cur_num = cur_num // 2
    return res[::-1]


def main():
    k = int(input())
    text = []
    for i in range(2 ** k):
        text.append(turn_to_2_sys(i, k))
    res = do_str_reconstruction(k, text)
    print(res[:-(k-1)])


if __name__ == '__main__':
    main()