import numpy as np
import sys


def find_coin_number(M, coins):
    num_coins = np.zeros(M)
    for coin in coins:
        if (coin <= M):
            num_coins[coin - 1] = 1
    for m in range(1, M + 1):
        min_num = sys.maxsize
        if (m not in coins):
            for coin in coins:
                if (m - coin >= 0):
                    if (num_coins[m - coin - 1] + 1 < min_num):
                        min_num = num_coins[m - coin - 1] + 1
            num_coins[m - 1] = min_num
    result = num_coins[M - 1]
    return int(result)


def final_result_hw21(M, text):
    real_coins = []
    cur_coin = ""
    for j in range(len(text)):
        if(text[j] == ","):
            real_coins.append(int(cur_coin))
            cur_coin = ""
        else:
            cur_coin += text[j]
    real_coins.append(int(cur_coin))

    res = find_coin_number(M, real_coins)
    print(res)


def main():
    M = int(input())
    coins = input()
    final_result_hw21(M, coins)


if __name__ == '__main__':
    main()