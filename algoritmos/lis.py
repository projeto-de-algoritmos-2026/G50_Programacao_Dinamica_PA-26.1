def maior_subsequencia_crescente(vetor):
    n = len(vetor)

    dp = [1] * n
    pre = [-1] * n

    for i in range(n):
        for j in range(i):
            if vetor[j] < vetor[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                pre[i] = j

    indice_final = dp.index(max(dp))

    return vetor, dp, pre, indice_final


def reconstruir_lis(L, pre, i):
    solucao = []

    while i != -1:
        solucao.append(L[i])
        i = pre[i]

    solucao.reverse()
    return solucao