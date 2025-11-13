# Compmon

Um jogo de batalha em 2D inspirado em Pokémon, desenvolvido em Python com a biblioteca Pygame. O projeto foi criado como parte de um trabalho acadêmico sobre Inteligência Artificial, com foco na implementação de um agente inteligente com múltiplos níveis de dificuldade e capacidade de aprendizado.

## 🎮 Sobre o Projeto

**Compmon** é um jogo onde duas criaturas batalham em turnos até que uma delas seja derrotada. O projeto possui um sistema completo de tipos, vantagens, ataques com dano e efeitos de status (como poison, sleep, freeze).

Na v1 do jogo não era possível jogar contra bots. Eu reformulei os códigos e inseri agentes inteligentes para representar níveis diferentes de dificuldade.

O jogo oferece dois modos principais:

- **Player vs. Player (PvP)**: Um modo local onde dois jogadores podem batalhar um contra o outro.
- **Player vs. IA (PvE)**: O modo central do projeto, onde o jogador enfrenta um agente inteligente com diferentes níveis de desafio.

## 🤖 O Agente Inteligente (IA)

O núcleo deste trabalho é o desenvolvimento de um oponente controlado por computador que simula um jogador estratégico. A IA foi projetada com três níveis de dificuldade distintos para testar diferentes abordagens de algoritmos de tomada de decisão.

### Nível 1: Fácil (Estratégia Aleatória)
A IA neste nível não possui nenhuma lógica estratégica. A cada turno, ela simplesmente escolhe um de seus quatro ataques de forma completamente aleatória. É um oponente imprevisível, mas fácil de superar, ideal para jogadores iniciantes.

### Nível 2: Médio (Estratégia Gulosa)
Neste nível, a IA utiliza um algoritmo guloso (Greedy). A cada turno, ela analisa todos os seus ataques que causam dano e escolhe aquele que infligirá a maior quantidade de dano imediato ao oponente, considerando as fraquezas de tipo. Ela sempre busca a jogada mais vantajosa para o presente momento, sem planejar o futuro.

### Nível 3: Difícil (Estratégia Minimax + Aprendizado)
O nível mais avançado combina duas técnicas de IA para criar um oponente desafiador e adaptativo:

**Algoritmo Minimax**: A IA consegue "olhar um turno à frente". Ela simula cada uma de suas possíveis jogadas e, para cada uma, calcula a melhor resposta possível do jogador. Ela então escolhe o movimento que a deixa na melhor posição possível, mesmo após sofrer o melhor contra-ataque do oponente. Isso a permite fazer sacrifícios táticos e se preparar para o turno seguinte.

**Aprendizado por Reforço (Simplificado)**: Esta é a característica mais avançada. A IA aprende com a experiência.

- Durante uma batalha, ela memoriza todos os ataques que utilizou.
- Ao final da partida, ela é informada se venceu ou perdeu.
- Ela atualiza um arquivo de memória (`memoria_ia.json`), registrando quais movimentos foram usados em batalhas vitoriosas ou em derrotas.
- Com o tempo, a IA ajusta sua estratégia. Se ela perceber que usar um determinado ataque de status frequentemente resulta em derrota, ela dará menos prioridade a esse ataque no futuro, mesmo que a tática Minimax o sugira. Isso a torna um oponente que se adapta ao meta do jogo.

## 🛠️ Tecnologias Utilizadas

- **Python 3.9+**
- **Pygame 2.5.2**: Para a engine do jogo, renderização de gráficos, controle de input e áudio.
- **JSON**: Para armazenar e gerenciar os dados do jogo de forma estruturada (criaturas, ataques, efeitos e a memória da IA).

## 🚀 Como Executar o Projeto

Siga os passos abaixo para executar o Compmon em sua máquina local.

### 1. Clone o Repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
cd SEU_REPOSITORIO
```

### 2. Crie um Ambiente Virtual (Recomendado)
Isso mantém as dependências do projeto isoladas.

```bash
# Para Windows
python -m venv venv
.\venv\Scripts\activate

# Para macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências
O projeto depende principalmente da biblioteca Pygame.

```bash
pip install pygame
```

*Opcional: Se você criar um arquivo `requirements.txt` com `pygame==2.5.2` dentro, pode usar `pip install -r requirements.txt`*

### 4. Execute o Jogo
O ponto de entrada do jogo é o arquivo `main.py` dentro da pasta `codigos`.

```bash
python codigos/main.py
```


## 🔮 Melhorias Futuras

Este projeto tem uma base sólida que permite várias expansões interessantes:

- **IA mais Profunda**: Implementar um Minimax com maior profundidade (mais turnos à frente) e otimizá-lo com poda Alfa-Beta.
- **Sistema de "PP"**: Fazer com que os ataques tenham uma quantidade limitada de usos, adicionando uma camada extra de gerenciamento de recursos.
- **Mecânica de Troca**: Permitir que os jogadores (e a IA) tenham uma equipe de criaturas e possam trocá-las durante a batalha.
- **Animações Mais Complexas**: Criar um sistema de animação baseado em spritesheets para movimentos mais fluidos.
