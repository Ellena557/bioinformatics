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
            res[letter][elem] += (1 / len(mat))
    return res


def profile_prob_kmer(text, k, profile):
    best_pat = text[:k]
    bin_prof = make_probs_in_profile(profile)
    best_res = 0
    for i in range(len(text) - k + 1):
        pat = []
        for j in range(k):
            pat.append(text[i + j])
        cur_res = 1
        for l in range(k):
            ind = get_pos(pat[l])
            cur_res *= bin_prof[ind][l]
        if cur_res > best_res:
            best_pat = pat
            best_res = cur_res
    return best_pat


def find_hamming_dist(g1, g2):
    cur_sum = 0
    for i in range(len(g1)):
        if (g1[i] != g2[i]):
            cur_sum += 1
    return cur_sum


def rev_lexic_order(p):
    if (p == 0):
        return "A"
    else:
        if (p == 3):
            return "T"
        else:
            if (p == 1):
                return "C"
            else:
                return "G"


def NumberToPattern(num, k):
    pat = ""
    n = num
    for i in range(k):
        let = n % 4
        n = n // 4
        pat += rev_lexic_order(let)
    return pat[::-1]


def fill_pats(k):
    pats = []
    for i in range(4 ** k):
        pats.append(NumberToPattern(i, k))
    return pats


def find_d_st(pat, st):
    ham = len(pat)
    for j in range(len(st) - len(pat) + 1):
        pat2 = []
        for i in range(len(pat)):
            pat2.append(st[i + j])
        ham2 = find_hamming_dist(pat, pat2)
        if (ham > ham2):
            ham = ham2
    return ham


def find_d(pat, Dna):
    d = 0
    for st in Dna:
        d += find_d_st(pat, st)
    return d


def find_median_string(Dna):
    probs = make_probs_in_profile(Dna)
    median = ""
    for i in range(len(Dna[0])):
        cur_arr = []
        for j in range(4):
            cur_arr.append(probs[j][i])
        max_el = np.argmax(np.array(cur_arr))
        median += rev_lexic_order(max_el)
    return median


def get_score(mat, k):
    cons = find_median_string(mat)
    scor = get_scor_fast(mat, cons)
    return scor

def get_scor_fast(mat, cons):
    res = 0
    for st in mat:
        for i in range(len(st)):
            if st[i] != cons[i]:
                res += 1
    return res

def do_greedy_motif_search(Dna, k, t):
    best_motifs = []
    for st in Dna:
        best_motifs.append(st[:k])
    best_score = get_score(best_motifs, k) + 1000
    for i in range(len(Dna[0]) - k + 1):
        motif1 = Dna[0][i: i + k]
        cur_motifs = []
        cur_motifs.append(motif1)
        for j in range(1, t):
            cur_mot = profile_prob_kmer(Dna[j], k, cur_motifs)
            cur_motifs.append(cur_mot)
        cur_score = get_score(cur_motifs, k)
        # if(cur_score) > 0:
        #    print(cur_motifs)
        if (cur_score < best_score):
            best_motifs = cur_motifs
            best_score = cur_score
    return best_motifs


def final_result_hw6(text, k, t):
    res = do_greedy_motif_search(text, k, t)
    for i in range(len(res)):
        st = ""
        for j in range(len(res[i])):
            st += res[i][j]
        print(st)


def main():
    k = int(input())
    t = int(input())
    text = []
    for i in range(t):
        n = input()
        text.append(n)
    final_result_hw6(text, k, t)


if __name__ == '__main__':
    main()