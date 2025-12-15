"""Estruturas e operações de Árvore AVL.

Extende a BST com balanceamento automático por rotações após inserções
ou remoções, garantindo altura O(log n).
"""

from binaria_de_busca import NoBST, ArvoreBST


class NoAVL(NoBST):
    """Nó de uma Árvore AVL.

    Herda de ``NoBST`` e adiciona `altura` e `fator_balanceamento`.
    """

    def __init__(self, chave: int):
        super().__init__(chave)
        self.altura = 1
        self.fator_balanceamento = 0

    def __str__(self) -> str:
        return f"{self.chave} (Altura: {self.altura}, FB: {self.fator_balanceamento})"

    def atualizar(self) -> None:
        """Atualiza a altura e o fator de balanceamento do nó."""
        altura_esquerda = self.esquerda.altura if self.esquerda else 0
        altura_direita = self.direita.altura if self.direita else 0
        self.altura = 1 + max(altura_esquerda, altura_direita)
        self.fator_balanceamento = altura_esquerda - altura_direita


class ArvoreAVL(ArvoreBST):
    """Árvore AVL balanceada por rotações.

    Mantém |fator_balanceamento| <= 1 para todos os nós.
    Usa ``NoAVL`` como tipo de nó e as rotações herdadas da BST,
    com atualização de altura/fator a cada ajuste.
    """

    def __init__(self):
        super().__init__(NoAVL)

    def _rotacao_direita(self, no_atual: NoAVL) -> None:
        """Rotação à direita com atualização de altura/FB.

        Args:
            no_atual (NoAVL): Nó pivô da rotação.
        """
        novo_pai = no_atual.esquerda
        super()._rotacao_direita(no_atual)
        no_atual.atualizar()
        if novo_pai:
            novo_pai.atualizar()

    def _rotacao_esquerda(self, no_atual: NoAVL) -> None:
        """Rotação à esquerda com atualização de altura/FB.

        Args:
            no_atual (NoAVL): Nó pivô da rotação.
        """
        novo_pai = no_atual.direita
        super()._rotacao_esquerda(no_atual)
        no_atual.atualizar()
        if novo_pai:
            novo_pai.atualizar()

    def _reequilibrar(self, no: NoAVL) -> None:
        """Reequilibra subárvores de baixo para cima a partir de ``no``.

        Aplica rotações simples ou duplas nos casos LL/LR e RR/RL,
        atualizando altura e fator de balanceamento após cada rotação.
        """
        while no:
            no.atualizar()

            if no.fator_balanceamento > 1:
                if no.esquerda and no.esquerda.fator_balanceamento < 0:
                    self._rotacao_esquerda(no.esquerda)
                self._rotacao_direita(no)

            elif no.fator_balanceamento < -1:
                if no.direita and no.direita.fator_balanceamento > 0:
                    self._rotacao_direita(no.direita)
                self._rotacao_esquerda(no)

            no = no.pai

    def inserir(self, chave: int) -> None:
        """Insere uma ``chave`` e reequilibra a árvore se necessário.

        Args:
            chave (int): Chave a inserir.
        """
        novo_no = super()._inserir(chave)
        if novo_no:
            self._reequilibrar(novo_no)

    def remover(self, chave: int) -> None:
        """Remove a ``chave`` e reequilibra a árvore se necessário.

        Args:
            chave (int): Chave a remover.
        """
        pai_do_removido = super()._remover(chave)
        if pai_do_removido:
            self._reequilibrar(pai_do_removido)
