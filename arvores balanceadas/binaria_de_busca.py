"""Módulo que implementa uma árvore Binária de Busca."""


class NoBST:
    """No da árvore Binária de Busca."""

    def __init__(self, chave: int):
        self.chave: int = chave
        self.esquerda: NoBST | None = None
        self.direita: NoBST | None = None
        self.pai: NoBST | None = None

    def __str__(self) -> str:
        return f"{self.chave}"


class ArvoreBST:
    """Representa uma árvore Binária de Busca."""

    def __init__(self, no=NoBST):
        self.raiz = None
        self.no = no

    def _rotacao_direita(self, no_atual: NoBST) -> None:
        """Método para realizar uma rotação à direita em um nó.
        Args:
            no_atual (NoBST): Nó atual onde a rotação será realizada.
        """
        no_avo = no_atual.pai
        novo_pai = no_atual.esquerda
        novo_filho = novo_pai.direita

        # Atualiza o ponteiro do avo para o novo pai
        if no_avo is None:
            self.raiz = novo_pai
        elif no_avo.chave < no_atual.chave:
            no_avo.direita = novo_pai
        else:
            no_avo.esquerda = novo_pai

        # Atualiza os ponteiros do novo pai
        novo_pai.pai = no_avo
        novo_pai.direita = no_atual

        # Atualiza os ponteiros do nó atual
        no_atual.pai = novo_pai
        no_atual.esquerda = novo_filho

        # Atualiza o ponteiro do novo filho, se existir
        if novo_filho is not None:
            novo_filho.pai = no_atual

    def _rotacao_esquerda(self, no_atual: NoBST) -> None:
        """Método para realizar uma rotação à esquerda em um nó.
        Args:
            no_atual (NoBST): Nó atual onde a rotação será realizada.
        """
        no_avo = no_atual.pai
        novo_pai = no_atual.direita
        novo_filho = novo_pai.esquerda

        # Atualiza o ponteiro do avo para o novo pai
        if no_avo is None:
            self.raiz = novo_pai
        elif no_avo.chave < no_atual.chave:
            no_avo.direita = novo_pai
        else:
            no_avo.esquerda = novo_pai

        # Atualiza os ponteiros do novo pai
        novo_pai.pai = no_avo
        novo_pai.esquerda = no_atual

        # Atualiza os ponteiros do nó atual
        no_atual.pai = novo_pai
        no_atual.direita = novo_filho

        # Atualiza o ponteiro do novo filho, se existir
        if novo_filho is not None:
            novo_filho.pai = no_atual

    def _inserir(self, chave: int) -> NoBST:
        """Método para inserir um nó com a chave especificada na árvore.
        Args:
            chave (int): Chave a ser inserida na árvore.
        Returns:
            NoBST: Retorna o nó inserido.
        """
        novo_no = self.no(chave)

        if self.raiz is None:
            self.raiz = novo_no
            return novo_no

        # Encontrar a posição correta para o novo nó
        no_atual = self.raiz
        while no_atual is not None:
            pai = no_atual
            if novo_no.chave < no_atual.chave:
                no_atual = no_atual.esquerda
            else:
                no_atual = no_atual.direita

        # Inserir o novo nó
        novo_no.pai = pai
        if novo_no.chave < pai.chave:
            pai.esquerda = novo_no
        else:
            pai.direita = novo_no

        return novo_no

    def _sucessor(self, no: NoBST) -> NoBST:
        """Método para encontrar o sucessor de um nó.
        Args:
            no (NoBST): Nó para o qual o sucessor será encontrado.
        Returns:
            NoBST: Nó sucessor encontrado.
        """
        atual = no.direita
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual

    def _antecessor(self, no: NoBST) -> NoBST:
        """Método para encontrar o antecessor de um nó.
        Args:
            no (NoBST): Nó para o qual o antecessor será encontrado.
        Returns:
            NoBST: Nó antecessor encontrado.
        """
        atual = no.esquerda
        while atual.direita is not None:
            atual = atual.direita
        return atual

    def _remover(self, chave: int) -> NoBST | None:
        """Método para remover um nó com a chave especificada da árvore.
        Args:
            chave (int): Chave do nó a ser removido.
        Returns:
            NoBST | None: Nó pai do nó removido que pode precisar ser reequilibrado.
        """
        no_a_remover = self.buscar(chave)
        if no_a_remover is None:
            return None

        # Caso 1 e 2: Nó com 0 ou 1 filho
        if no_a_remover.esquerda is None or no_a_remover.direita is None:
            # Obtém o nó pai antes de remover, será necessário para reequilibrar
            pai_do_removido = no_a_remover.pai

            if no_a_remover.esquerda:
                novo_filho = no_a_remover.esquerda
            else:
                novo_filho = no_a_remover.direita

            # Removendo a raiz
            if pai_do_removido is None:
                self.raiz = novo_filho
            else:
                # Conecta o pai do nó removido diretamente ao neto
                if no_a_remover == pai_do_removido.esquerda:
                    pai_do_removido.esquerda = novo_filho
                else:
                    pai_do_removido.direita = novo_filho

            # Atualiza o pai do novo filho, se existir
            if novo_filho is not None:
                novo_filho.pai = pai_do_removido

        # Caso 3: Nó com dois filhos
        else:
            sucessor = self._sucessor(no_a_remover)
            chave_sucessor = sucessor.chave
            # Remove o sucessor e substitui a chave do nó a remover
            pai_do_removido = self._remover(sucessor.chave)
            no_a_remover.chave = chave_sucessor

        # retorna o nó pai do removido que precisar ser reequilibrado
        return pai_do_removido

    def _buscar(self, no_atual: NoBST | None, chave: int) -> NoBST | None:
        """Método para buscar um nó com a chave especificada na árvore.
        Args:
            no_atual (NoBST | None): Nó atual na recursão da busca.
            chave (int): Chave do nó a ser buscado.
        Returns:
            NoBST | None: Nó encontrado ou None se não existir.
        """
        if no_atual is None or no_atual.chave == chave:
            return no_atual
        elif chave < no_atual.chave:
            return self._buscar(no_atual.esquerda, chave)
        else:
            return self._buscar(no_atual.direita, chave)

    def _pre_ordem(self, no: NoBST) -> list:
        """Método que gera a lista de elementos da ávore em pré-ordem
        Args:
            no (NoBST): Nó atual na recursão.
        Returns:
            list: Lista de chaves em pré-ordem.
        """
        if no is None:
            return []
        resultado = [no.chave]
        resultado.extend(self._pre_ordem(no.esquerda))
        resultado.extend(self._pre_ordem(no.direita))
        return resultado

    def _em_ordem(self, no: NoBST) -> list:
        """Método que gera a lista de elementos da árvore em ordem
        Args:
            no (NoBST): Nó atual na recursão.
        Returns:
            list: Lista de chaves em ordem.
        """
        if no is None:
            return []
        resultado = self._em_ordem(no.esquerda)
        resultado.append(no.chave)
        resultado.extend(self._em_ordem(no.direita))
        return resultado

    def _pos_ordem(self, no: NoBST) -> list:
        """Método que gera a lista de elementos da árvore em pós-ordem
        Args:
            no (NoBST): Nó atual na recursão.
        Returns:
            list: Lista de chaves em pós-ordem.
        """
        if no is None:
            return []
        resultado = self._pos_ordem(no.esquerda)
        resultado.extend(self._pos_ordem(no.direita))
        resultado.append(no.chave)
        return resultado

    def buscar(self, chave: int) -> NoBST | None:
        """Método que busca uma chave dentro da árvore
        Args:
            chave (int): chave a ser buscada.
        Returns:
            NoBST | None: Nó encontrado ou None se não existir.
        """
        return self._buscar(self.raiz, chave)

    def mostrar(self, ordem: str = "em_ordem") -> list:
        """Método que seleciona a forma da árvore a ser mostrada
        Args:
            ordem (str, optional): tipo da ordem a ser mostrada. Defaults to "em_ordem".
        Raises:
            ValueError: Caso o argumento passado não esteja dentre as opções
        Returns:
            list: Lista com as chaves de acordo com a ordem selecionada
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
