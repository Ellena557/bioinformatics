def find_hamming_dist(g1, g2):
    cur_sum = 0
    for i in range(len(g1)):
        if (g1[i] != g2[i]):
            cur_sum += 1
    return cur_sum


def find_approx_pattern_match(p, text, d):
    all_ids = []
    for i in range(len(text) - len(p) + 1):
        p2 = []
        for j in range(len(p)):
            p2.append(text[i + j])
        if (find_hamming_dist(p, p2) <= d):
            all_ids.append(i)
    return all_ids


def final_result_hw3(p, text, d):
    res = find_approx_pattern_match(p, text, d)
    st = ""
    for i in range(len(res)):
        st += str(res[i])
        st += " "
    print(st)


def main():
    p = input()
    text = input()
    d = int(input())
    final_result_hw3(p, text, d)


if __name__ == '__main__':
    main()