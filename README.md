PROJETO POKEMON 

1 - Definir atributos das Criaturas:
HP
Nome da criatura
Elementos da criatura ( 9 elementos )
Pokémon de dois tipos (opcional)
Speed (quem ataca primeiro)(opcional)
Algum outro atributo(opcional)

2 - Definir os ataques das criaturas
Nome dos ataques
Dano Causado
Tipo de ataque( corpo a corpo, a distância, opcional)
Efeitos especiais( paralisia, choque, opcional)
Limites de uso dos ataques na batalha( Acho legal por)
Criar uma lista de ataques neutros que podem ser usados por todos os pokémons e definir uma lista de ataques para cada tipo

3 - Implementar a Conexão Entre a Lista de criaturas e a Lista de ataques
Podemos fazer duas listas pique estrutura de dados clássica e fazer relação entre elas.
Podemos usar o JSON que foi recomendado lá no trabalho( estou fazendo com esse no início, se eu ver que vai ficar muito complicado eu troco)
Considerar o critério de uso dos ataques e habilidades específicas.

4 - PARTES FINAIS ( IMPLEMENTAR UMA INTERFACE)
Criar uma interface no terminal para os jogadores interagir
O jogador que vai escolher sua criatura e os ataques da criatura (MAX 4) de uma lista de ataques para aqueles Pokémon escolhido
Temos que colocar informações importantes durante a batalha como a vida que os bichos estão, ataques realizados e efeitos causados.
Seria legal também se não deixarmos ver o pokémon que o outro escolheu para não ter vantagem na escolha

5 - Fazer a lógica de batalha 
Temos que dar um jeito de fazer um sistema de turnos até a vida de um pokémon estiver zerada (PENSO EM FAZER TIPO UMA MD3 e quem ganhar duas vezes leva)
Temos que Calcular o dano causado com base nos atributos, vantagem e nos ataques escolhidos ( vai dar uma escada de if else enorme)
Verificar se alguma das criaturas atingiu vida zero ao final de cada turno.

6 - DESAFIOS PARA FAZER SE TIVER TEMPO (Que tava no doc deles)
Implementar um sistema de netplay para permitir conexão local via hamachi, logmein, coisas desse tipo.
Criar uma interface gráfica para o jogo, deixá-lo mais visual.
