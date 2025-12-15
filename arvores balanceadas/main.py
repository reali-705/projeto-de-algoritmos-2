"""Módulo principal para manipulação de árvores balanceadas."""

from avl import ArvoreAVL
from rubro_negro import ArvoreRubroNegro


def escolher_opcao(opcoes: list) -> int:
    """Exibe menu numerado e retorna escolha validada do usuário.

    Força entrada válida dentro do intervalo de opções.

    Args:
        opcoes (list): Lista de strings com opções disponíveis.

    Returns:
        int: Índice (0-based) da opção escolhida.
    """
    escolhas = "\n".join(f"({chave}) {valor}" for chave, valor in enumerate(opcoes))
    while True:
        opcao_selecionada = input(
            f"\nEscolha um número entre as opções:\n{escolhas}\nOpção: "
        )
        try:
            resposta = int(opcao_selecionada)
            if resposta not in range(len(opcoes)):
                print("Opção inválida. Tente novamente.")
                continue
            return resposta
        except ValueError:
            print("Entrada inválida. Por favor, insira um número válido.")


def acao_arvore(arvore: ArvoreAVL | ArvoreRubroNegro) -> None:
    """Executa ação selecionada na árvore (inserir, buscar, remover, mostrar).

    Mantém loop até usuário escolher sair ou mudar de árvore. Valida entradas
    e exibe resultados (busca, percursos).

    Args:
        arvore (ArvoreAVL | ArvoreRubroNegro): Árvore para operar.
    """
    while True:
        acao = [
            "Voltar ao menu de árvores",
            "Inserir",
            "Buscar",
            "Remover",
            "Mostrar percursos",
        ]
        escolha = escolher_opcao(acao)

        match escolha:
            case 0:
                return
            case 1:
                try:
                    chave = int(input("Digite a chave a inserir: "))
                    arvore.inserir(chave)
                    print(f"Chave {chave} inserida com sucesso.")
                except ValueError:
                    print("Entrada inválida. Digite um número inteiro.")
            case 2:
                try:
                    chave = int(input("Digite a chave a buscar: "))
                    resultado = arvore.buscar(chave)
                    if resultado:
                        print(f"Chave {chave} encontrada: {resultado}")
                    else:
                        print(f"Chave {chave} não encontrada na árvore.")
                except ValueError:
                    print("Entrada inválida. Digite um número inteiro.")
            case 3:
                try:
                    chave = int(input("Digite a chave a remover: "))
                    arvore.remover(chave)
                    print(f"Chave {chave} removida com sucesso.")
                except ValueError:
                    print("Entrada inválida. Digite um número inteiro.")
            case 4:
                try:
                    pre = arvore.mostrar("pre_ordem")
                    em = arvore.mostrar("em_ordem")
                    pos = arvore.mostrar("pos_ordem")
                    print(f"\nPré-Ordem: {', '.join(map(str, pre))}\n")
                    print(f"Em-Ordem: {', '.join(map(str, em))}\n")
                    print(f"Pós-Ordem: {', '.join(map(str, pos))}\n")
                except ValueError:
                    print("Erro ao mostrar percursos: entrada inválida.")


def main() -> None:
    """Inicializa loop principal para seleção e manipulação de árvores.

    Permite escolher entre AVL ou Rubro-Negra, realizar ações, e sair.
    Continua até usuário escolher "Parar".
    """
    while True:
        arvores = ["Parar", "AVL", "Rubro-Negro"]
        escolha = escolher_opcao(arvores)

        match escolha:
            case 0:
                print("Encerrando programa.")
                break
            case 1:
                print("Árvore AVL selecionada.\n")
                arvore = ArvoreAVL()
                acao_arvore(arvore)
            case 2:
                print("Árvore Rubro-Negra selecionada.\n")
                arvore = ArvoreRubroNegro()
                acao_arvore(arvore)


if __name__ == "__main__":
    main()
