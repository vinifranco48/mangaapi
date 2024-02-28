class Edit_Distance_Custom:
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
        self.memo = {}  # Dicionário para memoização dos resultados

    def distance(self):
        return self._distance(len(self.s1), len(self.s2))

    def _distance(self, i, j):
        if (i, j) in self.memo:
            return self.memo[(i, j)]

        # Caso base: se uma das strings estiver vazia, a distância é o comprimento da outra string
        if i == 0:
            return j
        if j == 0:
            return i

        # Se os últimos caracteres são iguais, a distância é igual à distância sem os últimos caracteres
        if self.s1[i - 1] == self.s2[j - 1]:
            dist = self._distance(i - 1, j - 1)
        else:
            # Caso contrário, considere as operações de inserção, deleção e substituição
            dist = 1 + min(
                self._distance(i, j - 1),  # Inserção
                self._distance(i - 1, j),  # Deleção
                self._distance(i - 1, j - 1)  # Substituição
            )

        self.memo[(i, j)] = dist
        return dist