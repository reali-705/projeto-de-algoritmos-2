"""Estruturas e operações de Árvore Rubro-Negra (RB-tree).

Mantém propriedades de balanceamento via cores (vermelho/preto) e rotações,
garantindo altura O(log n). Suporta busca, inserção, remoção e validação
de altura-negra.
"""

from binaria_de_busca import NoBST, ArvoreBST


class NoRN(NoBST):
    """Nó de uma Árvore Rubro-Negra.

    Herda de ``NoBST`` e adiciona:
    - `cor`: ``True`` (vermelho) ou ``False`` (preto); padrão vermelho.
    - `altura_negra`: número de nós pretos no caminho mais curto até folha.
    """

    def __init__(self, chave: int, cor: bool = True):
        super().__init__(chave)
        self.cor = cor
        self.altura_negra = 1

    def __str__(self) -> str:
        return f"{self.chave} ({'V' if self.cor else 'P'}, AN: {self.altura_negra})"

    def atualizar(self) -> None:
        """Atualiza altura-negra baseada nas subárvores.

        Altura-negra é o número de nós pretos até a folha mais próxima.
        Se filhos têm alturas-negras diferentes, retorna -1 (inválido).
        """
        altura_negra_esquerda = self.esquerda.altura_negra if self.esquerda else 1
        altura_negra_direita = self.direita.altura_negra if self.direita else 1

        if (
            altura_negra_esquerda == -1
            or altura_negra_direita == -1
            or altura_negra_esquerda != altura_negra_direita
        ):
            self.altura_negra = -1
        else:
            self.altura_negra = altura_negra_esquerda + (0 if self.cor else 1)


class ArvoreRubroNegro(ArvoreBST):
    """Árvore Rubro-Negra balanceada por cores e rotações.

    Propriedades:
    - Raiz é sempre preta.
    - Nós vermelhos não têm filhos vermelhos.
    - Todos os caminhos raiz -> folha têm igual número de nós pretos (altura-negra).
    - Garante altura máxima 2*log(n+1).
    """

    def __init__(self):
        super().__init__(NoRN)

    def _cor_vermelha(self, no: NoRN | None) -> bool:
        """Verifica se ``no`` é vermelho (nós nulos são pretos).

        Args:
            no (NoRN | None): Nó a verificar.

        Returns:
            bool: ``True`` se vermelho, ``False`` se preto ou ``None``.
        """
        return no.cor if no else False

    def _balancear(self, no: NoRN) -> None:
        """Corrige violações de cores após inserção (cascata bottom-up).

        Caso 1 (tio vermelho): recolore pai, tio e avó, propaga para cima.
        Caso 2 (tio preto): rotações simples/duplas (LL/LR/RR/RL), recolore.
        Garante: raiz preta, nós vermelhos sem filhos vermelhos.

        Args:
            no (NoRN): Nó inserido; começa detecção de violação.
        """

        while no.pai is not None and self._cor_vermelha(no.pai):
            pai = no.pai
            avo = pai.pai

            if pai == avo.esquerda:
                tio = avo.direita
            else:
                tio = avo.esquerda

            if self._cor_vermelha(tio):
                pai.cor = False
                tio.cor = False
                avo.cor = True

                pai.atualizar()
                tio.atualizar()

                no = avo

            else:
                if no == pai.direita:
                    no = pai
                    self._rotacao_esquerda(no)
                    no.atualizar()
                    pai = no.pai
                    avo = pai.pai

                pai.cor = False
                avo.cor = True
                self._rotacao_direita(avo)
                pai.atualizar()
                avo.atualizar()

        self.raiz.cor = False
        if self.raiz:
            self.raiz.atualizar()

    def inserir(self, chave: int) -> None:
        """Insere uma ``chave`` e balanceia cores/rotações se necessário.

        Novo nó é inicializado vermelho; em seguida, ``_balancear()`` garante
        propriedades RB.

        Args:
            chave (int): Chave a inserir.
        """
        novo_no = super()._inserir(chave)
        if novo_no:
            self._balancear(novo_no)

    def remover(self, chave: int) -> None:
        """Remove a ``chave`` e balanceia cores/altura-negra se necessário.

        Usa método herdado ``_remover()`` e, se uma remoção afetou
        altura-negra, chama ``_balancear_remocao()`` para restaurar
        propriedades RB (especialmente altura-negra).

        Args:
            chave (int): Chave a remover.
        """
        pai_do_removido = super()._remover(chave)
        if pai_do_removido:
            self._balancear_remocao(pai_do_removido)

        if self.raiz:
            self.raiz.cor = False
            self.raiz.atualizar()

    def _balancear_remocao(self, no: NoRN | None) -> None:
        """Corrige violações de altura-negra após remoção (cascata bottom-up).

        Se nó é preto com apenas 1 filho, rotações/recolorações restauram
        propriedades. Se raiz, garante que é preta.

        Args:
            no (NoRN | None): Nó pai do removido; inicia cascata de correção.
        """
        while no is not None and no != self.raiz:
            if no.esquerda and not self._cor_vermelha(no):
                irmao = no.direita
                if irmao and self._cor_vermelha(irmao):
                    irmao.cor = False
                    no.cor = True
                    self._rotacao_esquerda(no)
                    no.atualizar()
                    irmao.atualizar()
                    irmao = no.direita
                if irmao:
                    if not self._cor_vermelha(
                        irmao.esquerda
                    ) and not self._cor_vermelha(irmao.direita):
                        irmao.cor = True
                        irmao.atualizar()
                        no = no.pai
                    else:
                        if not self._cor_vermelha(irmao.direita):
                            if irmao.esquerda:
                                irmao.esquerda.cor = False
                            irmao.cor = True
                            self._rotacao_direita(irmao)
                            irmao.atualizar()
                            irmao = no.direita
                        if irmao:
                            irmao.cor = no.cor
                            no.cor = False
                            if irmao.direita:
                                irmao.direita.cor = False
                            self._rotacao_esquerda(no)
                            no.atualizar()
                            irmao.atualizar()
                            no = self.raiz
            else:
                no = no.pai
        if self.raiz:
            self.raiz.cor = False
            self.raiz.atualizar()

    def _contar_pretos(self, no: NoRN | None) -> int:
        """Conta nós pretos no caminho da raiz até ``no`` (incluindo ``no``).

        Args:
            no (NoRN | None): Nó final do caminho.

        Returns:
            int: Quantidade de nós pretos (1 se ``no`` é ``None``).
        """
        if no is None:
            return 1
        return (1 if not no.cor else 0) + self._contar_pretos(no.esquerda)

    def _altura_negra(self, no: NoRN | None) -> int:
        """Retorna altura-negra de ``no`` (nós pretos até folha mais próxima).

        Todos os caminhos de ``no`` até folha devem ter mesma altura-negra
        para árvore RB válida.

        Args:
            no (NoRN | None): Raiz da subárvore a medir.

        Returns:
            int: Altura-negra, ou -1 se inválida (caminhos diferentes).
        """
        if no is None:
            return 1
        altura_negra_esquerdaura = self._altura_negra(no.esquerda)
        altura_negra_direitaura = self._altura_negra(no.direita)
        if (
            altura_negra_esquerdaura == -1
            or altura_negra_direitaura == -1
            or altura_negra_esquerdaura != altura_negra_direitaura
        ):
            return -1
        return altura_negra_esquerdaura + (1 if not no.cor else 0)

    def validar_propriedades(self) -> bool:
        """Valida todas as propriedades de uma Árvore Rubro-Negra.

        Verifica:
        - Raiz é preta.
        - Nós vermelhos não têm filhos vermelhos.
        - Altura-negra igual em todos os caminhos.

        Returns:
            bool: ``True`` se todas as propriedades são satisfeitas.
        """
        if self.raiz is None:
            return True
        if self.raiz.cor:
            return False
        if not self._validar_vermelho(self.raiz):
            return False
        return self._altura_negra(self.raiz) >= 1

    def _validar_vermelho(self, no: NoRN | None) -> bool:
        """Verifica se nós vermelhos não têm filhos vermelhos (recursivo).

        Args:
            no (NoRN | None): Nó a verificar.

        Returns:
            bool: ``True`` se nenhuma violação encontrada.
        """
        if no is None:
            return True
        if self._cor_vermelha(no):
            if self._cor_vermelha(no.esquerda) or self._cor_vermelha(no.direita):
                return False
        return self._validar_vermelho(no.esquerda) and self._validar_vermelho(
            no.direita
        )
