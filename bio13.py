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


def find_euler_path(graph, d):
    # the form of a graph here will be definitely a euler graph -> no need for extra check
    edges = graph[1]
    verts = graph[0]
    degrees = np.zeros(len(verts))
    idx_of_start_vtx = 0

    for i in range(len(verts)):
        for j in range(len(verts)):
            degrees[i] += edges[i][j]
            degrees[j] -= edges[i][j]

    for v in range(len(verts)):
        if (degrees[v] == 1):
            idx_of_start_vtx = v

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
        cur_pref1 = pat[0][:-1]
        cur_suf1 = pat[0][1:]
        cur_pref2 = pat[1][:-1]
        cur_suf2 = pat[1][1:]

        if ([cur_pref1, cur_pref2] in vertices):
            idx_pref = vertices.index([cur_pref1, cur_pref2])
        else:
            idx_pref = len(vertices)
            vertices.append([cur_pref1, cur_pref2])
        if ([cur_suf1, cur_suf2] in vertices):
            idx_suf = vertices.index([cur_suf1, cur_suf2])
        else:
            idx_suf = len(vertices)
            vertices.append([cur_suf1, cur_suf2] )
        all_edges[idx_pref][idx_suf] += 1
    return vertices, all_edges


def do_str_reconstruction(k, d, text):
    db_graph = make_db_graph(text)
    eul_path = find_euler_path(db_graph, d)
    res = compine_genom_from_path(eul_path, d, k)
    return res


def final_result_hw13(k, d, text):
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
    final_result_hw13(k, d, text)


if __name__ == '__main__':
    main()