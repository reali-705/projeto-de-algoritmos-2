"""Estruturas e operações de Árvore Binária de Busca (BST).

Inclui o nó (`NoBST`) e a árvore (`ArvoreBST`) com operações
de rotação, busca, inserção, remoção e percursos (pré, em e pós-ordem).
"""


class NoBST:
    """Nó de uma Árvore Binária de Busca.

    Armazena a `chave` e referências para os filhos (`esquerda`, `direita`)
    e para o `pai`.
    """

    def __init__(self, chave: int):
        self.chave: int = chave
        self.esquerda: NoBST | None = None
        self.direita: NoBST | None = None
        self.pai: NoBST | None = None

    def __str__(self) -> str:
        return f"{self.chave}"


class ArvoreBST:
    """Árvore Binária de Busca (BST).

    - Mantém a propriedade da BST: chaves menores à esquerda e maiores à direita.
    - Suporta rotações locais, busca, inserção, remoção e percursos.

    Args:
        no: classe ou fábrica de nós a ser utilizada (padrão: ``NoBST``).
    """

    def __init__(self, no=NoBST):
        self.raiz = None
        self.no = no

    def _rotacao_direita(self, no_atual: NoBST) -> None:
        """Realiza uma rotação à direita tendo ``no_atual`` como pivô.

        Args:
            no_atual (NoBST): Nó que será o pivô da rotação.
        """
        no_avo = no_atual.pai
        novo_pai = no_atual.esquerda
        novo_filho = novo_pai.direita

        if no_avo is None:
            self.raiz = novo_pai
        elif no_avo.chave < no_atual.chave:
            no_avo.direita = novo_pai
        else:
            no_avo.esquerda = novo_pai

        novo_pai.pai = no_avo
        novo_pai.direita = no_atual

        no_atual.pai = novo_pai
        no_atual.esquerda = novo_filho

        if novo_filho is not None:
            novo_filho.pai = no_atual

    def _rotacao_esquerda(self, no_atual: NoBST) -> None:
        """Realiza uma rotação à esquerda tendo ``no_atual`` como pivô.

        Args:
            no_atual (NoBST): Nó que será o pivô da rotação.
        """
        no_avo = no_atual.pai
        novo_pai = no_atual.direita
        novo_filho = novo_pai.esquerda

        if no_avo is None:
            self.raiz = novo_pai
        elif no_avo.chave < no_atual.chave:
            no_avo.direita = novo_pai
        else:
            no_avo.esquerda = novo_pai

        novo_pai.pai = no_avo
        novo_pai.esquerda = no_atual

        no_atual.pai = novo_pai
        no_atual.direita = novo_filho

        if novo_filho is not None:
            novo_filho.pai = no_atual

    def _inserir(self, chave: int) -> NoBST | None:
        """Insere um novo nó com a ``chave`` na BST.

        Args:
            chave (int): Chave a ser inserida.

        Returns:
            NoBST | None: O nó inserido, ou ``None`` se a chave já existir.
        """
        if self.buscar(chave) is not None:
            return None

        novo_no = self.no(chave)

        if self.raiz is None:
            self.raiz = novo_no
            return novo_no

        no_atual = self.raiz
        while no_atual is not None:
            pai = no_atual
            if novo_no.chave < no_atual.chave:
                no_atual = no_atual.esquerda
            else:
                no_atual = no_atual.direita

        novo_no.pai = pai
        if novo_no.chave < pai.chave:
            pai.esquerda = novo_no
        else:
            pai.direita = novo_no

        return novo_no

    def _sucessor(self, no: NoBST) -> NoBST:
        """Retorna o sucessor in-order de ``no`` (menor nó da subárvore direita)."""
        atual = no.direita
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def _antecessor(self, no: NoBST) -> NoBST:
        """Retorna o antecessor in-order de ``no`` (maior nó da subárvore esquerda)."""
        atual = no.esquerda
        while atual.direita is not None:
            atual = atual.direita
        return atual

    def _remover(self, chave: int) -> NoBST | None:
        """Remove o nó com a ``chave`` e retorna o nó potencialmente afetado.

        Args:
            chave (int): Chave a remover.

        Returns:
            NoBST | None: Pai do nó removido, que pode precisar de reequilíbrio.
        """
        no_a_remover = self.buscar(chave)
        if no_a_remover is None:
            return None

        # Caso 1 e 2: Nó com 0 ou 1 filho
        if no_a_remover.esquerda is None or no_a_remover.direita is None:
            pai_do_removido = no_a_remover.pai

            if no_a_remover.esquerda:
                novo_filho = no_a_remover.esquerda
            else:
                novo_filho = no_a_remover.direita

            if pai_do_removido is None:
                self.raiz = novo_filho
            else:
                if no_a_remover == pai_do_removido.esquerda:
                    pai_do_removido.esquerda = novo_filho
                else:
                    pai_do_removido.direita = novo_filho

            if novo_filho is not None:
                novo_filho.pai = pai_do_removido

        # Caso 3: Nó com dois filhos
        else:
            sucessor = self._sucessor(no_a_remover)
            chave_sucessor = sucessor.chave
            pai_do_removido = self._remover(sucessor.chave)
            no_a_remover.chave = chave_sucessor

        return pai_do_removido

    def _buscar(self, no_atual: NoBST | None, chave: int) -> NoBST | None:
        """Busca recursiva por um nó com a ``chave`` dada.

        Args:
            no_atual (NoBST | None): Raiz da subárvore atual.
            chave (int): Chave desejada.

        Returns:
            NoBST | None: Nó encontrado, ou ``None`` se não existir.
        """
        if no_atual is None or no_atual.chave == chave:
            return no_atual
        elif chave < no_atual.chave:
            return self._buscar(no_atual.esquerda, chave)
        else:
            return self._buscar(no_atual.direita, chave)

    def _pre_ordem(self, no: NoBST) -> list:
        """Gera a lista de chaves da árvore em pré-ordem.

        Args:
            no (NoBST): Nó atual na recursão.

        Returns:
            list: Chaves em pré-ordem.
        """
        if no is None:
            return []
        resultado = [no]
        resultado.extend(self._pre_ordem(no.esquerda))
        resultado.extend(self._pre_ordem(no.direita))
        return resultado

    def _em_ordem(self, no: NoBST) -> list:
        """Gera a lista de chaves da árvore em ordem (in-order).

        Args:
            no (NoBST): Nó atual na recursão.

        Returns:
            list: Chaves em ordem.
        """
        if no is None:
            return []
        resultado = self._em_ordem(no.esquerda)
        resultado.append(no)
        resultado.extend(self._em_ordem(no.direita))
        return resultado

    def _pos_ordem(self, no: NoBST) -> list:
        """Gera a lista de chaves da árvore em pós-ordem.

        Args:
            no (NoBST): Nó atual na recursão.

        Returns:
            list: Chaves em pós-ordem.
        """
        if no is None:
            return []
        resultado = self._pos_ordem(no.esquerda)
        resultado.extend(self._pos_ordem(no.direita))
        resultado.append(no)
        return resultado

    def buscar(self, chave: int) -> NoBST | None:
        """Busca uma ``chave`` na árvore e retorna o nó correspondente.

        Args:
            chave (int): Chave desejada.

        Returns:
            NoBST | None: Nó encontrado, ou ``None`` se não existir.
        """
        return self._buscar(self.raiz, chave)

    def mostrar(self, ordem: str = "em_ordem") -> list:
        """Retorna as chaves conforme a ordem solicitada.

        Args:
            ordem (str, optional): Uma entre ``"pre_ordem"``, ``"em_ordem"`` (padrão)
                ou ``"pos_ordem"``.

        Returns:
            list: Chaves na ordem escolhida.

        Raises:
            ValueError: Se ``ordem`` não for uma das opções válidas.
        """
        if ordem == "pre_ordem":
            return self._pre_ordem(self.raiz)
        elif ordem == "em_ordem":
            return self._em_ordem(self.raiz)
        elif ordem == "pos_ordem":
            return self._pos_ordem(self.raiz)
        else:
            raise ValueError(
                "Ordem inválida. Use 'pre_ordem', 'em_ordem' ou 'pos_ordem'."
            )
