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


def do_generate_motif(dna_str, k, prof_mat):
    all_probs = []
    for i in range(len(dna_str) - k + 1):
        cur_pat = []
        for j in range(k):
            cur_pat.append(dna_str[i + j])
        cur_res = 1
        for j in range(k):
            let = get_pos(cur_pat[j])
            cur_prob = prof_mat[let][j]
            cur_res *= cur_prob
        all_probs.append(cur_res)

    sum_prob = np.sum(all_probs)

    all_probs = all_probs / sum_prob

    rand_motif_idx = int(np.random.choice(a = np.arange(0, len(dna_str) - k + 1), size = 1, p = np.array(all_probs)))
    return dna_str[rand_motif_idx : rand_motif_idx + k]


def do_gibbs_sampler(Dna, k, t, N):
    motifs = []
    for i in range(t):
        idx = np.random.randint(low=0, high=len(Dna[0]) - k + 1)
        motifs.append(Dna[i][idx: idx + k])
    best_motifs = motifs
    best_score = get_score(best_motifs, k)

    for time in range(N):
        dna_idx = np.random.randint(low=0, high=t)
        prof_mat = make_probs_in_profile(motifs)
        motif_idx = do_generate_motif(Dna[dna_idx], k, prof_mat)
        motifs[dna_idx] = motif_idx
        cur_score = get_score(motifs, k)
        if (cur_score < best_score):
            best_motifs = motifs
            best_score = cur_score
            #print(best_score)
    return best_motifs, best_score


def final_result_hw9(text, k, t, N):
    res = (text, k, t, N)
    best_mots = res[0]

    num_starts = 20

    best_scor = res[1]
    for start_num in range(num_starts - 1):
        cur_res = do_gibbs_sampler(text, k, t, N)
        cur_mots = cur_res[0]
        cur_scor = cur_res[1]
        if (cur_scor < best_scor):
            best_mots = cur_mots
            best_scor = cur_scor

    for i in range(len(best_mots)):
        st = ""
        for j in range(len(best_mots[i])):
            st += best_mots[i][j]
        print(st)
    #print(best_scor, " !!!! ")


def main():
    k = int(input())
    t = int(input())
    N = int(input())
    text = []
    for i in range(t):
        n = input()
        text.append(n)
    final_result_hw9(text, k, t, N)


if __name__ == '__main__':
    main()