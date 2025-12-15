"""Módulo que implementa uma árvore AVL."""

from binaria_de_busca import NoBST, ArvoreBST


class NoAVL(NoBST):
    """No da árvore AVL."""

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
    """Representa uma árvore AVL."""

    def __init__(self):
        super().__init__(NoAVL)

    def _rotacao_direita(self, no_atual: NoAVL) -> None:
        novo_pai = no_atual.esquerda
        super()._rotacao_direita(no_atual)
        no_atual.atualizar()
        if novo_pai:
            novo_pai.atualizar()

    def _rotacao_esquerda(self, no_atual: NoAVL) -> None:
        novo_pai = no_atual.direita
        super()._rotacao_esquerda(no_atual)
        no_atual.atualizar()
        if novo_pai:
            novo_pai.atualizar()

    def _reequilibrar(self, no: NoAVL) -> None:
        """Reequilibra a árvore a partir do nó fornecido."""
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

    def inserir(self, chave) -> None:
        """Insere um valor na árvore AVL e reequilibra a árvore se necessário."""
        self._reequilibrar(super()._inserir(chave))

    def remover(self, chave) -> None:
        """Remove um valor da árvore AVL e reequilibra a árvore se necessário."""
        pai_do_removido = super()._remover(chave)
        if pai_do_removido:
            # Reequilibra a partir do pai do nó removido
            self._reequilibrar(pai_do_removido)
