import numpy as np


def do_expand(peptide):
    all_mass = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]
    expand_peptide = []
    for j in range(len(all_mass)):
        cur_pep = []
        for t in range(len(peptide)):
            cur_pep.append(peptide[t])
        cur_pep.append(all_mass[j])
        expand_peptide.append(cur_pep)
    return expand_peptide


def count_peptide_mass(peptide):
    return np.sum(peptide)


def count_parent_mass(spec):
    return np.max(spec)


def generate_sybpeptides(peptide):
    res = []
    res.append(0)
    n = len(peptide)
    extra_peptide = peptide + peptide
    for j in range(1, n):
        for i in range(n):
            cur_subpeptide = np.sum(extra_peptide[i : i + j])
            res.append(cur_subpeptide)
    res.append(np.sum(peptide))
    return res


def find_cyclospectrum(peptide):
    spec = generate_sybpeptides(peptide)
    return np.sort(spec)


def is_consistent(peptide, spec):
    is_cons = 1
    for i in range(len(peptide)):
        for j in range(1, len(peptide) - i + 1):
            if (np.sum(peptide[i : i + j]) not in spec):
                is_cons = 0
    return is_cons


def check_that_arrays_are_equal(a, b):
    is_eq = 1
    for i in range(len(a)):
        if (a[i] != b[i]):
            is_eq = 0
    return is_eq


def do_cyclopeptide_sequencing(spec):
    candidates = [[]]
    final_res = []

    while(len(candidates) > 0):
        cur_ok_candidates = []
        for cand in candidates:
            next_candidates = do_expand(cand)
            new_next_candidates = []
            for j in range(len(next_candidates)):
                new_next_candidates.append(next_candidates[j])

            for cur_pep in next_candidates:
                if (count_peptide_mass(cur_pep) == count_parent_mass(spec)):
                    cur_spec = find_cyclospectrum(cur_pep)
                    if (check_that_arrays_are_equal(cur_spec, spec) == 1):
                        if (cur_pep not in final_res):
                            final_res.append(cur_pep)
                    new_next_candidates.remove(cur_pep)
                else:
                    if (is_consistent(cur_pep, spec) == 0):
                        new_next_candidates.remove(cur_pep)

            for c in new_next_candidates:
                cur_ok_candidates.append(c)
        candidates = cur_ok_candidates
    return final_res


def final_result_hw18(text):
    spec = []
    cur_num = ""
    for j in range(len(text)):
        if(text[j] == " "):
            spec.append(int(cur_num))
            cur_num = ""
        else:
            cur_num += text[j]
    spec.append(int(cur_num))
    res = do_cyclopeptide_sequencing(spec)

    st_res = ""
    for r in res:
        for i in range(len(r)):
            st_res += str(r[i])
            if (i < len(r) - 1):
                st_res += "-"
        st_res += " "
    print(st_res)


def main():
    text = input()
    final_result_hw18(text)


if __name__ == '__main__':
    main()