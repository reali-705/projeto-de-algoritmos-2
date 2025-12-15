# Árvores Balanceadas

Implementação completa de estruturas de árvores balanceadas com operações eficientes de inserção, remoção, busca e percursos.

## Estruturas Implementadas

### Árvore Binária de Busca (BST) - Superclasse Base

[**Arquivo:** `binaria_de_busca.py`](./binaria_de_busca.py)

Implementação base que serve como **superclasse para reaproveitamento de código** em estruturas derivadas (AVL, Rubro-Negra).

**Operações:**

- Rotações direita/esquerda (primitivas usadas por subclasses)
- Busca, inserção e remoção O(n)
- Percursos: pré-ordem, em-ordem, pós-ordem
- Métodos privados `_buscar()`, `_inserir()`, `_remover()`, `_sucessor()`, `_antecessor()`

**Complexidade:**

- Pior caso (desbalanceada): O(n)
- Melhor caso (balanceada): O(log n)

---

### Árvore AVL

[**Arquivo:** `avl.py`](./avl.py)

Herda de BST com **balanceamento automático por altura**.

**Propriedades:**

- Cada nó mantém `altura` e `fator_balanceamento` (diferença de altura entre filhos)
- |fator_balanceamento| ≤ 1 em todos os nós
- Rotações simples (LL, RR) e duplas (LR, RL) aplicadas conforme necessário

**Operações:**

- `inserir(chave)`: insere e reequilibra bottom-up
- `remover(chave)`: remove e reequilibra bottom-up
- `_reequilibrar(no)`: corrige desbalanços identificando tipo de rotação

**Complexidade Garantida:**

- Altura máxima: O(log n)
- Operações (busca, inserção, remoção): O(log n)

**Exemplo de Exibição (via `NoAVL.__str__()`):**

```bash
5 (Altura: 2, FB: 0)
10 (Altura: 1, FB: 0)
```

---

### Árvore Rubro-Negra

[**Arquivo:** `rubro_negro.py`](./rubro_negro.py)

Herda de BST com **balanceamento por cores e propriedades estruturais**.

**Propriedades RB:**

1. Raiz é sempre **preta**
2. Nós vermelhos **não têm filhos vermelhos** (sem red-red adjacency)
3. Todos os caminhos raiz→folha têm **igual número de nós pretos** (altura-negra uniforme)
4. Nós nulos contam como pretos

**Atributos de Nó:**

- `cor`: `True` (vermelho) ou `False` (preto)
- `altura_negra`: número de nós pretos até folha mais próxima

**Operações:**

- `inserir(chave)`: insere (vermelho) e reequilibra por cores via cascata bottom-up
  - Caso 1 (tio vermelho): recoloração (pai, tio, avó)
  - Caso 2 (tio preto): rotações simples/duplas + recoloração

- `remover(chave)`: remove e restaura altura-negra via rotações/recolorações

- `validar_propriedades()`: verifica raiz preta, ausência de red-red, altura-negra uniforme

**Complexidade Garantida:**

- Altura máxima: 2×log(n+1)
- Operações (busca, inserção, remoção): O(log n)

**Exemplo de Exibição (via `NoRN.__str__()`):**

```bash
5 (V, AN: 1)    # vermelho, altura-negra 1
10 (P, AN: 2)   # preto, altura-negra 2
```

---

## Como Executar

```bash
cd "arvores balanceadas"
python main.py
```

**Menu interativo:**

1. Escolha o tipo de árvore (AVL ou Rubro-Negra)
2. Realize operações:
   - Inserir chave
   - Buscar chave
   - Remover chave
   - Mostrar percursos (pré, em, pós-ordem)

## Exemplos de Código

### AVL

```python
from avl import ArvoreAVL

arvore = ArvoreAVL()
arvore.inserir(10)
arvore.inserir(20)
arvore.inserir(5)
arvore.inserir(15)

# Buscar
no = arvore.buscar(10)
print(no)  # Exibe: "10 (Altura: 2, FB: 0)"

# Percursos
print(arvore.mostrar("pre_ordem"))  # 10 (Altura: 2, FB: 0), 5 (Altura: 1, FB: 0), 20 (Altura: 1, FB: 0), 15 (Altura: 1, FB: 0)
print(arvore.mostrar("em_ordem"))   # 5 (Altura: 1, FB: 0), 10 (Altura: 2, FB: 0), 15 (Altura: 1, FB: 0), 20 (Altura: 1, FB: 0)
print(arvore.mostrar("pos_ordem"))  # 5 (Altura: 1, FB: 0), 15 (Altura: 1, FB: 0), 20 (Altura: 1, FB: 0), 10 (Altura: 2, FB: 0)

# Remover
arvore.remover(20)
```

### Rubro-Negra

```python
from rubro_negro import ArvoreRubroNegra

arvore = ArvoreRubroNegra()
arvore.inserir(7)
arvore.inserir(3)
arvore.inserir(18)

# Buscar
no = arvore.buscar(7)
print(no)  # Exibe: "7 (P, AN: 1)" (conforme NoRN.__str__())

# Validar propriedades
valido = arvore.validar_propriedades()
print(f"Árvore válida: {valido}")

# Percursos
print(arvore.mostrar("pre_ordem"))  # 7 (P, AN: 1), 3 (P, AN: 1), 18 (P, AN: 1)
print(arvore.mostrar("em_ordem"))   # 3 (P, AN: 1), 7 (P, AN: 1), 18 (P, AN: 1)
print(arvore.mostrar("pos_ordem"))  # 3 (P, AN: 1), 18 (P, AN: 1), 7 (P, AN: 1)

# Remover
arvore.remover(3)
```

---

## Formato de Exibição

A **forma de exibição dos nós** segue exatamente o **método `__str__()`** de cada classe:

- **BST/AVL:** mostra apenas a chave
- **NoAVL (AVL):** `chave (Altura: X, FB: Y)` — altura e fator de balanceamento
- **NoRN (Rubro-Negra):** `chave (C, AN: X)` — cor (V=vermelho, P=preto) e altura-negra

Assim, ao buscar, inserir ou trabalhar com nós individualmente, a representação em string reflete o estado atual da estrutura.

---

## Requisitos Técnicos

- **Python:** 3.10+ (union type hints `|`)
- **Padrões:** PEP 257 (docstrings), type hints completos
- **Estrutura:** Herança, polimorfismo, encapsulamento

---

## Reaproveitamento de Código

A classe `ArvoreBST` (BST base) fornece:

- Rotações primitivas (`_rotacao_direita`, `_rotacao_esquerda`)
- Inserção/remoção base (`_inserir`, `_remover`)
- Percursos (`_pre_ordem`, `_em_ordem`, `_pos_ordem`)
- Busca recursiva (`_buscar`)

**Subclasses (AVL, Rubro-Negra):**

- Herdam e reutilizam rotações
- Adicionam métodos de balanceamento específicos
- Sobrescrevem `inserir()` e `remover()` para chamar lógica de reequilíbrio

Isso **minimiza duplicação** e facilita manutenção.

---

## Validação de Propriedades

- AVL
  - Verifica fator de balanceamento em cascata (via `_reequilibrar`)

- Rubro-Negra

  - `validar_propriedades()`: valida raiz preta + ausência de red-red + altura-negra uniforme
  - `_validar_vermelho()`: recursivo, detecta filhos vermelhos de nó vermelho
  - `_altura_negra()`: calcula altura-negra, retorna -1 se inválida (caminhos diferentes)
