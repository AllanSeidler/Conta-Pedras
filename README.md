# Conta-Pedras
Ideia inicial: Utilizar 2 etapas para realizar a aplicação da IA

## Etapa 1: Identificar as pedras do jogo
Nesta etapa será feita a identificação das pedras do jogo. Isto será feito por meio de uma rede neural que recebe como entrada um conjunto dos seguintes dados:
1. Posição corrente de cada uma das 7 pedras do jogo, denotadas por:
	- números de "1" a "7" para identificar a posição da pedra na pista.
	- "F" para identificar que está fora da pista.
	- "?" para identificar que a posição dessa pedra é desconhecida, ou seja, está oculta. 

2. A(s) ultima(s) 1/3/5 ações realizadas (intercalando oponente/jogador). 
	- O número de ações determina a memória da IA, bem como a dificuldade do jogo.
	- Estas ações podem ser nulas, identificando que não 
	- As ações são definidas formalmente pela tupla: (id, p1, p2), onde:
		- id: É o id da ação realizada.
		- p1: É a posição da 1° peça interagida.\*
		- p2: É a posição da 2° peça interagida.\*

3. Como saída e esperado um conjunto de 7 pedras, semelhante as 7 pedras de entrada. Porém, com pedras denotas por "?" possivelmente reveladas.

\*: Estes valores podem ser nulos/ausentes.

## Etapa 2: Definir a proxima ação
Para definir a proxima ação será feito a utilização de clusteres que dividirá os dados da etapa anterior unidos com os dados de ações de "espiar" realizadas pelo oponente. Como saida é esperado uma tupla de ação. Igual a utilizada como entrada.

---

Vale notar que, estaremos fazendo uso de aprendizado supervisionado durante a primeira etapa. Contudo, durante a segunda etapa não há uma saída esperada, o que indica o uso de aprendizado não supervisionado.
