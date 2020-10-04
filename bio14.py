import numpy as np


def compine_genom_from_path(path):
    res = ""
    for i in range(len(path)):
        res += path[i][0]
    k = len(path[0])
    res += path[len(path) - 1][1:]
    return res


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


def find_incom_edges(graph, vert):
    edges = graph[1]
    verts = graph[0]
    income_edges = 0
    for j in range(len(verts)):
        income_edges += (edges[j][vert])
    return income_edges


def find_contigs(graph):
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

    all_contigs = []

    for v in range(len(verts)):
        #cur_contig = []
        cur_vert = v

        income_edges = 0
        for j in range(len(verts)):
            income_edges += (edges[j][cur_vert])

        #no outcoming edges
        if (np.sum(edges[cur_vert]) == 0):
            continue

        #only 1 outcoming edge and 1 incoming edge
        if ((np.sum(edges[cur_vert]) == 1) and (income_edges == 1)):
            continue

        out_edges = []
        for j in range(len(verts)):
            if (edges[v][j] > 0):
                for t in range(int(edges[v][j])):
                    out_edges.append(j)

        for j in out_edges:
            if (edges[v][j] > 0):
                cur_contig = []
                cur_contig.append(v)
                cur_contig.append(j)
                cur_vert = j

                # while the path is nonbranching
                while ((np.sum(edges[cur_vert]) == 1) and (find_incom_edges(graph, cur_vert) == 1) and (len(cur_contig) < len(verts))):
                    for u in range(len(verts)):
                        if (edges[cur_vert][u] == 1):
                            cur_contig.append(u)
                            cur_vert = u
                            break
                all_contigs.append(cur_contig)

    res_pats = []
    for i in range(len(all_contigs)):
        cur_pat = []
        for j in range(len(all_contigs[i])):
            cur_pat.append(verts[all_contigs[i][j]])
        res_pats.append(cur_pat)

    return res_pats


def do_generate_all_contigs(k, text):
    db_graph = make_db_graph(text)
    res_contigs = find_contigs(db_graph)
    res = ""
    for c in range(len(res_contigs)):
        res += compine_genom_from_path(res_contigs[c])
        res += " "
    return res


def main():
    inext = 1
    text = []
    while (inext == 1):
        t = input()
        if (t == "-1"):     # it's a signal that is is the end of the text!
            inext = 0
        else:
            text.append(t)
    k = len(text[0])
    res = do_generate_all_contigs(k, text)
    print(res)


if __name__ == '__main__':
    main()