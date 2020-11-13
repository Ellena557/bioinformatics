import numpy as np


def do_range_expand(peptides, alphabet):
    expand_peptides = []
    for p in range(len(peptides)):
        for j in range(len(alphabet)):
            cur_pep = []
            for t in range(len(peptides[p])):
                cur_pep.append(peptides[p][t])
            cur_pep.append(alphabet[j])
            expand_peptides.append(cur_pep)
    return expand_peptides


def count_peptide_mass(peptide):
    return np.sum(peptide)


def count_parent_mass(spec):
    if (len(spec) == 0):
        return 0
    return np.max(spec)


def generate_sybpeptides(peptide):
    res = []
    res.append(0)
    n = len(peptide)
    extra_peptide = peptide + peptide
    for j in range(1, n):
        for i in range(n):
            cur_subpeptide = sum(extra_peptide[i : i + j])
            res.append(cur_subpeptide)
    res.append(np.sum(peptide))
    return res


def find_score(peptide, spec):
    if (len(peptide) == 0):
        return len(spec)
    pep_spec = generate_sybpeptides(peptide)
    ex_spec = []
    for i in range(len(spec)):
        ex_spec.append(spec[i])
    scor = 0
    for elem in pep_spec:
        if (elem in ex_spec):
            ex_spec.remove(elem)
            scor += 1
    return scor


def do_trim(leaders, spec, N):
    if (len(leaders) <= N):
        return leaders

    sorted_leaders = sorted(leaders, key=lambda p: find_score(p, spec))
    res = sorted_leaders[len(sorted_leaders) - N:]
    return res


def do_leaderboard_cyclopeptide_sequencing(spec, N, alphabet):
    leaders = [[]]
    cur_leader = []
    cur_top_score = 0
    parent_mass = count_parent_mass(spec)
    while (len(leaders) > 0):
        #leaders = do_expand(leaders)
        leaders = do_range_expand(leaders, alphabet)
        next_leaders = []
        for j in range(len(leaders)):
            next_leaders.append(leaders[j])

        for cur_pep in leaders:
            cur_mass = count_peptide_mass(cur_pep)
            if (cur_mass == parent_mass):
                cur_score = find_score(cur_pep, spec)
                if ( cur_score > cur_top_score):
                    cur_leader = cur_pep
                    cur_top_score = cur_score
                    #print("Leader: ", cur_leader, "   ----     ", cur_top_score)
            else:
                if (cur_mass > parent_mass):
                    next_leaders.remove(cur_pep)

        leaders = do_trim(next_leaders, spec, N)
    return cur_leader


def get_alphabet(M, spec):
    differences = []
    for i in range(len(spec) - 1):
        for j in range(i+1, len(spec)):
            differences.append(int((np.abs(spec[i] - spec[j]))))

    alphabet = []
    for pept in spec:
        if (pept >= 57 and pept <= 200):
            alphabet.append(pept)

    for pept in differences:
        if (pept >= 57 and pept <= 200):
            alphabet.append(pept)

    alp_counts = np.zeros(201)
    for pept in alphabet:
        alp_counts[pept] += 1

    sorted_alphabet = sorted(alphabet, key=lambda k: alp_counts[k])
    sorted_unique_alphabet = []
    sorted_unique_alphabet.append(sorted_alphabet[0])
    sorted_unique_alphabet = []
    sorted_unique_alphabet.append(sorted_alphabet[0])
    for i in range(1, len(sorted_alphabet)):
        if (sorted_alphabet[i] not in sorted_unique_alphabet):
            sorted_unique_alphabet.append(sorted_alphabet[i])
    if (len(sorted_unique_alphabet) > M):
        sorted_unique_alphabet = sorted_unique_alphabet[len(sorted_unique_alphabet) - M:]
    return sorted_unique_alphabet


def do_convolution_cyclopeptide_sequencing(M, N, spec):
    alph = get_alphabet(M, spec)
    res = do_leaderboard_cyclopeptide_sequencing(spec, N, alph)
    return res


def final_result_hw20(M, N, text):
    spec = []
    cur_num = ""
    for j in range(len(text)):
        if(text[j] == " "):
            spec.append(int(cur_num))
            cur_num = ""
        else:
            cur_num += text[j]
    spec.append(int(cur_num))

    res = do_convolution_cyclopeptide_sequencing(M, N, spec)
    st_res = ""
    for r in range(len(res)):
        st_res += str(res[r])
        if (r < len(res) - 1):
            st_res += "-"
    print(st_res)


def main():
    M = int(input())
    N = int(input())
    text = input()
    final_result_hw20(M, N, text)


if __name__ == '__main__':
    main()