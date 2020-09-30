import numpy as np


def compine_genom_from_path(path):
    res = ""
    for i in range(len(path)):
        res += path[i][0]
    k = len(path[0])
    res += path[len(path) - 1][1:]
    return res


def find_euler_path(graph):
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
    #cycle_ids.append(idx_of_start_vtx)

    not_visited_verts = []
    not_visited_verts.append(idx_of_start_vtx)

    while(len(not_visited_verts) > 0):
        cur_vert = not_visited_verts[0]

        if (degrees[cur_vert] == 0):
            cycle_ids.append(cur_vert)
            not_visited_verts.pop(0)
        else:
            for j in range(len(verts)):
                if (edges[cur_vert][j] > 0):
                    not_visited_verts.append(j)
                    edges[cur_vert][j] -= 1
                    degrees[cur_vert] -= 1
                    degrees[j] += 1

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
    eul_path = find_euler_path(db_graph)
    res = compine_genom_from_path(eul_path)
    return res


def main():
    k = int(input())
    inext = 1
    text = []
    while (inext == 1):
        t = input()
        if (t == "-1"):     # it's a signal that is is the end of the text!
            inext = 0
        else:
            text.append(t)
    res = do_str_reconstruction(k, text)
    print(res)


if __name__ == '__main__':
    main()