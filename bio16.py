def translate_cod(cod):
    all_cods = {
        "AAA" : "K",
        "AAC" : "N",
        "AAG" : "K",
        "AAU" : "N",
        "ACA" : "T",
        "ACC" : "T",
        "ACG" : "T",
        "ACU" : "T",
        "AGA" : "R",
        "AGC" : "S",
        "AGG" : "R",
        "AGU" : "S",
        "AUA" : "I",
        "AUC" : "I",
        "AUG" : "M",
        "AUU" : "I",
        "CAA" : "Q",
        "CAC" : "H",
        "CAG" : "Q",
        "CAU" : "H",
        "CCA" : "P",
        "CCC" : "P",
        "CCG" : "P",
        "CCU" : "P",
        "CGA" : "R",
        "CGC" : "R",
        "CGG" : "R",
        "CGU" : "R",
        "CUA" : "L",
        "CUC" : "L",
        "CUG" : "L",
        "CUU" : "L",
        "GAA" : "E",
        "GAC" : "D",
        "GAG" : "E",
        "GAU" : "D",
        "GCA" : "A",
        "GCC" : "A",
        "GCG" : "A",
        "GCU" : "A",
        "GGA" : "G",
        "GGC" : "G",
        "GGG" : "G",
        "GGU" : "G",
        "GUA" : "V",
        "GUC" : "V",
        "GUG" : "V",
        "GUU" : "V",
        "UAA" : "",
        "UAC" : "Y",
        "UAG" : "",
        "UAU" : "Y",
        "UCA" : "S",
        "UCC" : "S",
        "UCG" : "S",
        "UCU" : "S",
        "UGA" : "",
        "UGC" : "C",
        "UGG" : "W",
        "UGU" : "C",
        "UUA" : "L",
        "UUC" : "F",
        "UUG" : "L",
        "UUU" : "F"
    }
    amin = all_cods[cod]
    return amin


def translate_rna_to_amin_acid(rna):
    res = ""
    for i in range(int(len(rna) / 3)):
        cur_cod = str(rna[3 * i : 3 * i + 3])
        cur_amin = translate_cod(cur_cod)
        res += cur_amin
    return res


def reverse_nuc(p):
    if (p == 'A'):
        return 'U'
    else:
        if (p == 'U'):
            return 'A'
        else:
            if (p == 'C'):
                return 'G'
            else:
                return 'C'


def reverse_rna(rna):
    rev_rna = ""
    for j in range(len(rna)):
        rev_rna += str(reverse_nuc(rna[j]))
    return rev_rna[::-1]


def turn_dna_to_rna(dna):
    rna = ""
    for j in range(len(str(dna))):
        if (str(dna)[j] == "T"):
            rna += "U"
        else:
            rna += str(dna)[j]
    return rna


def turn_rna_to_dna(rna):
    dna = ""
    for j in range(len(str(rna))):
        if (str(rna)[j] == "U"):
            dna += "T"
        else:
            dna += str(rna)[j]
    return dna


def do_peptide_encoding(dna, amins):
    rna = turn_dna_to_rna(dna)
    res = []
    pep_len = 3 * len(amins)
    for j in range(len(rna) - pep_len + 1):
        cur_pep = str(rna[j : j + pep_len])
        cur_amin = translate_rna_to_amin_acid(cur_pep)
        if (cur_amin == amins):
            res.append(turn_rna_to_dna(cur_pep))
        else:
            cur_pep_reversed = reverse_rna(cur_pep)

            cur_amin_rev = translate_rna_to_amin_acid(cur_pep_reversed)
            if (cur_amin_rev == amins):
                res.append(turn_rna_to_dna(cur_pep))
    return res


def main():
    dna = input()
    amins = input()
    res = do_peptide_encoding(dna, amins)
    for r in res:
        print(r)


if __name__ == '__main__':
    main()