import numpy as np


def get_pos(p):
    if (p == 'A'):
        return 0
    else:
        if (p == 'T'):
            return 3
        else:
            if (p == 'C'):
                return 1
            else:
                return 2


def make_probs_in_profile(mat):
    res = np.zeros((4, len(mat[0])))
    for row in mat:
        for elem in range(len(mat[0])):
            letter = get_pos(row[elem])
            res[letter][elem] += (1 / (len(mat) + 4))
    for i in range(4):
        for j in range(len(mat[0])):
            res[i][j] += (1 / (len(mat) + 4))
    return res


def find_hamming_dist(g1, g2):
    cur_sum = 0
    for i in range(len(g1)):
        if (g1[i] != g2[i]):
            cur_sum += 1
    return cur_sum


def get_score(mat, k):
    #cons = find_median_string(mat)
    scor = get_scor_prof(mat, k)
    return scor


def get_scor_prof(mat, k):
    all_letters = np.zeros((4, len(mat[0])))
    for st in range(len(mat[0])):
        for i in range(len(mat)):
            let = get_pos(mat[i][st])
            all_letters[let][st] += 1
    max_reses = np.zeros(len(mat[0]))

    for i in range(len(mat[0])):
        cur_column = []
        for j in range(4):
            cur_column.append(all_letters[j][i])
        max_reses[i] = np.max(cur_column)

    res = len(mat) * len(mat[0]) - np.sum(max_reses)
    return res


def get_motif(Dna, k, prof_mat):
    res = []
    for row in range(len(Dna)):
        best_prob = 0
        best_res = Dna[row][:k]
        for i in range(len(Dna[0]) - k + 1):
            cur_prob = 1
            for m in range(k):
                letter = get_pos(Dna[row][i + m])
                cur_prob *= prof_mat[letter][m]
            if (cur_prob > best_prob):
                best_prob = cur_prob
                best_res = Dna[row][i : i + k]
        res.append(best_res)
    return res


def do_randomized_motif_search(Dna, k, t):
    motifs = []
    for i in range(t):
        idx = np.random.randint(low=0, high=len(Dna[0]) - k + 1)
        motifs.append(Dna[i][idx: idx + k])
    best_motifs = motifs
    best_score = get_score(best_motifs, k)

    while (1 == 1):
        prof_mat = make_probs_in_profile(motifs)
        motifs = get_motif(Dna, k, prof_mat)
        cur_score = get_score(motifs, k)
        if (cur_score < best_score):
            best_motifs = motifs
            best_score = cur_score
            #print(best_score)
        else:
            return best_motifs, best_score
    return best_motifs, best_score


def final_result_hw8(text, k, t):
    first_res = do_randomized_motif_search(text, k, t)
    min_res = first_res[1]
    best_mots = first_res[0]
    for i in range(999):
        curr_res = do_randomized_motif_search(text, k, t)
        res = curr_res[1]
        if (res < min_res):
            min_res = res
            best_mots = curr_res[0]

    for i in range(len(best_mots)):
        st = ""
        for j in range(len(best_mots[i])):
            st += best_mots[i][j]
        print(st)


def main():
    k = int(input())
    t = int(input())
    text = []
    for i in range(t):
        n = input()
        text.append(n)
    final_result_hw8(text, k, t)


if __name__ == '__main__':
    main()