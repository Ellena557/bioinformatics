import numpy as np


def do_manhattan_pass(n, m, Down, Right):
    s_vals = np.zeros((n + 1, m + 1))

    for i in range(1, m + 1):
        s_vals[0][i] = Right[0][i-1] + s_vals[0][i-1]

    for i in range(1, n + 1):
        s_vals[i][0] = Down[i-1][0] + s_vals[i-1][0]

    for j in range(1, m + 1):
        for i in range(1, n + 1):
             s_vals[i][j] = np.max(np.array([s_vals[i-1][j] + Down[i-1][j], s_vals[i][j-1] + Right[i][j-1]]))

    result = s_vals[n][m]
    #print(s_vals)
    return int(result)


def final_result_hw22(n, m, text):
    Downs = np.zeros((n, m + 1))
    Rights = np.zeros((n + 1, m))
    for j in range(n):
        cur_i = 0
        cur_val = ""
        for i in range(len(text[j])):
            if(text[j][i] == " "):
                Downs[j][cur_i] = int(cur_val)
                cur_val = ""
                cur_i += 1
            else:
                cur_val += text[j][i]
        Downs[j][m] = cur_val

    for j in range(n + 1, 2 * n + 2):
        cur_i = 0
        cur_val = ""
        for i in range(len(text[j])):
            if(text[j][i] == " "):
                Rights[j - (n + 1)][cur_i] = int(cur_val)
                cur_val = ""
                cur_i += 1
            else:
                cur_val += text[j][i]
        Rights[j - (n + 1)][m - 1] = cur_val

    res = do_manhattan_pass(n, m, Downs, Rights)
    print(res)


def main():
    N = int(input())
    M = int(input())
    text = []
    for i in range(2 * N + 2):
        line = input()
        text.append(line)
    final_result_hw22(N, M, text)


if __name__ == '__main__':
    main()