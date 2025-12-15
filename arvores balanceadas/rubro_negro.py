"""Módulo que implementa uma árvore Rubro-Negro."""

from binaria_de_busca import NoBST, ArvoreBST


class NoRN(NoBST):
    """Representa o nó Rubro-Negro."""

    # True para vermelho, False para preto
    def __init__(self, chave: int, cor: bool = True):
        super().__init__(chave)
        self.cor = cor

    def __str__(self) -> str:
        return f"{self.chave} ({'V' if self.cor else 'P'})"

    def atualizar(self) -> None:
        """Atualiza a cor do nó Rubro-Negro."""


class AvoreNubroNegro(ArvoreBST):
    """Representa uma árvore Rubro-Negro."""

    def __init__(self):
        super().__init__(NoRN)

    def _cor_vermelha(self, no: NoRN | None) -> bool:
        """Método que retorna a cor do nó analisado
        Args:
            no (NoRN | None): Nó analisado
        Returns:
            bool: True para vermelho e False para preto
        """
        return no.cor if no else False

    def _minimo(self, no: NoRN) -> NoRN:
        """Método que retorna o nó com a menor chave a partir do nó dado.
        Args:
            no (NoRN): Nó a partir do qual buscar o mínimo
        Returns:
            NoRN: Nó com a menor chave
        """
        while no.esquerda is not None:
            no = no.esquerda
        return no

    def _transplantar(self, u: NoRN, v: NoRN | None) -> None:
        """Método que substitui a subárvore enraizada em u pela subárvore enraizada em v.
        Args:
            u (NoRN): Nó a ser substituído
            v (NoRN | None): Nó substituto
        """
        if u.pai is None:
            self.raiz = v
        elif u == u.pai.esquerda:
            u.pai.esquerda = v
        else:
            u.pai.direita = v
        if v is not None:
            v.pai = u.pai

    def _balancear(self, no: NoRN) -> None:
        """Mótodo que balanceia as cores da árvore rubro-negro.
        Args:
            no (NoRN): Nó modificado que começa o balanceamento
        """

        # Enquanto houver violação (Pai Vermelho e Nó Vermelho) e não for a raiz
        while no.pai is not None and self._cor_vermelha(no.pai):
            pai = no.pai
            # Se o pai é vermelho e não é raiz, o avô existe
            avo = pai.pai

            # Lado Esquerdo: Pai é filho à esquerda do Avô
            if pai == avo.esquerda:
                tio = avo.direita
            # Lado Direito: Pai é filho à direita do Avô
            else:
                tio = avo.esquerda

            # Caso 1: Tio é VERMELHO (Recolorir)
            if self._cor_vermelha(tio):
                pai.cor = False  # Pai vira Preto
                tio.cor = False  # Tio vira Preto
                avo.cor = True  # Avô vira Vermelho

                # Continua o looping caso a violação tenha subido para o avô
                no = avo

            # Caso 2: Tio é PRETO (Rotações)
            else:
                # Caso 2a: Nó é filho à direita (Zig-Zag) -> Rotação Dupla
                if no == pai.direita:
                    # Sobe a referencia para o pai para rotacionar
                    no = pai
                    self._rotacao_esquerda(no)
                    pai = no.pai
                    avo = pai.pai

                # Caso 2b: Nó é filho à esquerda (Linha Reta) -> Rotação Simples
                pai.cor = False  # Pai vira Preto
                avo.cor = True  # Avô vira Vermelho
                self._rotacao_direita(avo)

        # Propriedade: A raiz é sempre PRETA
        self.raiz.cor = False

    def inserir(self, chave: int) -> None:
        """Método que insere chave personalizado para a árvore rubro-negro.
        Args:
            chave (int): Chave a ser adiciona à árvore
        """
        self._balancear(super()._inserir(chave))

    def remover(self, chave: int) -> None:
        """Método que remove uma chave da árvore
        Args:
            chave (int): Chave a ser removida
        """
