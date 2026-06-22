# HENRY E A FLORESTA DO MUNDO - AVENTURA PELO TERMINAL

RPG de mesa textual em terminal feito para a atividade **Modelagem de Dados e Laboratório de Análise de Algorítmo**.

Henry viaja com Mitis para recuperar fragmentos mágicos da Árvore do Mundo.

## Como rodar

```bash
python main.py
```

Não precisa instalar bibliotecas externas.

## Como testar

```bash
python -m compileall -q .
python tests/smoke_test.py
```

## Requisitos atendidos

- TSP para calcular a melhor rota entre os locais da missão.
- Inventário como estrutura de dados.
- Coleta narrativa de itens nos locais do mapa, com pistas, escolhas e D20.
- MergeSort para ordenar o inventário.
- Loja da Capivara para compra e venda.
- Conversas com NPCs, incluindo rumores aleatórios da Capivara.
- Poções de HP e mana.
- Equipamentos com bônus de status e bônus elementais.
- Combate com magias de Henry e habilidades de Mitis.
- HUD de batalha separado entre grupo do jogador e inimigo.
- Quests dos aliados: Camila, Eduardo, Monique, Pietra e Santiago.
- Santiago como tucano navegador, liberado após cálculo da rota TSP.
- Progressão por EXP, level up e pontos de habilidade.
- Floresta Distorcida: dungeon paralela que muda a cada entrada.
- Save/load em JSON.
- Dungeon dinâmica: Floresta Distorcida, com salas aleatórias, eventos narrativos, acampamento com risco e mobs que escalam com o nível de Henry.

## Menu principal

O menu principal foi organizado em submenus para reduzir a poluição visual:

```txt
1 - Explorar
2 - Inventário
3 - Personagem
4 - Missões
5 - Sistema
0 - Sair
```

- **Explorar:** mapa, viagem, coleta, combate local, NPCs, Floresta Distorcida e Loja da Capivara.
- **Inventário:** ver, ordenar, consultar, usar consumível, equipar e remover itens.
- **Personagem:** status, habilidades e evolução.
- **Missões:** missão principal, rota TSP e quests dos aliados.
- **Sistema:** salvar, carregar e créditos.

## Personagens principais

### Henry

Henry, nosso protagonista, é um gato preto. No MVP, ele possui cinco famílias de magias ofensivas:

- **Fogo:** Fire → Fira → Firaga → Firaja.
- **Gelo:** Blizzard → Blizzara → Blizzaga → Blizzaja.
- **Trovão:** Thunder → Thundara → Thundaga → Thundaja.
- **Água:** Water → Watera → Waterga → Waterja.
- **Escuridão:** Dark → Darkra → Darkga → Darkja.

Essas magias usam mana do grupo e escalam com:

- atributo `magia`;
- nível da habilidade;
- bônus de equipamento;
- fraqueza ou resistência elemental do inimigo.

### Mitis

Mitis é o corujinha-buraqueira que acompanha Henry. Ele atua como suporte e mago de terra:

- **Terra:** Quake → Quakera → Quakega → Quakeja.
- **Cura:** Cure → Cura → Curaga → Curaja.
- **Remoção de status:** Esuna → Esunaga.
- **Tempo:** Haste → Hastera → Hastega.
- **Proteção física:** Protect → Protectga.
- **Proteção mágica:** Shell → Shellga.
- **Especial:** penas envenenadas, que causam dano inicial e veneno por turnos.

## Como a evolução das magias funciona

Ao subir de nível:

- os status base aumentam automaticamente por porcentagem;
- Henry ganha pontos de habilidade;
- os pontos podem ser gastos em famílias de magia.

Cada família possui subníveis antes de trocar para a próxima magia. Exemplo:

```txt
fire nível 0 → Fire
fire nível 1 → Fire I
fire nível 2 → Fire II
fire nível 3 → Fire III
fire nível 4 → Fira
```

A mesma regra vale para Blizzard, Thunder, Water, Dark, Quake, Cure, Haste, Protect e Shell.

## Coleta narrativa

A coleta não mostra mais uma lista direta de itens disponíveis. Em vez disso, o jogo apresenta uma cena curta de exploração:

```txt
Há um arbusto de formato estranho perto da trilha.
Mitis observa o lugar com atenção.

Deseja verificar o arbusto?
1 - Sim
2 - Não
```

Se Henry investigar, uma rolagem de D20 decide o resultado:

- **20:** encontra item e moedas.
- **12-19:** encontra item.
- **8-11:** nada útil acontece.
- **1-7:** Henry sofre uma consequência e perde HP.

## Floresta Distorcida

A Floresta Distorcida é uma dungeon. Ela muda a cada entrada e cada sala sorteia:

- um trecho da floresta;
- um arquétipo de mob;
- fraquezas e resistências elementais;
- recompensas possíveis.

Os mobs escalam com o nível de Henry e com a profundidade da exploração.

Além do combate normal, a Floresta pode disparar eventos narrativos:

- **Pedra Estranha:** investigação com D20, podendo gerar fragmentos, moedas ou dano.
- **Voz Distorcida:** Henry e Mitis podem seguir uma voz misteriosa para encontrar itens, recuperar mana ou sofrer dano.
- **Chão Desaparece:** evento de reflexo que pode devolver o grupo para a sala inicial.
- **Toca de Mitis:** evento raro em que Mitis entra em uma toca e Henry enfrenta combates sozinho enquanto Mitis investiga runas e um altar de Terra.
- **Acampamento:** depois de vencer uma sala, o jogador pode arriscar descansar. Um D20 define recuperação, penalidade ou emboscada.

Quando Mitis está separado, o combate mostra `BATALHA — HENRY` e bloqueia a opção de habilidades do Mitis.

Depois de vencer uma sala da Floresta, o jogador pode:

```txt
1 - Continuar mais fundo
2 - Acampar antes de continuar
3 - Sair da Floresta Distorcida
```

## Quests dos aliados

O MVP também possui um menu de quests dos personagens aliados:

- **Camila**, tamanduá-bandeira: quest no Bosque do Ipê envolvendo a Flor de Ipê e as formigas luminosas.
- **Eduardo**, jaguatirica: quest nas Ruínas da Arpia envolvendo investigação e combate contra a Pena Sombria.
- **Monique**, tatu-bola: quest na Caverna dos Golems envolvendo defesa e resistência.
- **Pietra**, onça-pintada: quest na Clareira da Árvore do Mundo para testar a evolução de Henry.
- **Santiago**, tucano navegador: quest na Vila das Preguiças que exige calcular a rota principal com TSP para liberar Santiago como navegador.

## Algoritmos

### TSP

Usado para calcular a menor rota da missão.
Complexidade da abordagem por força bruta:
```txt
O(n!)
```

### MergeSort

Usado para ordenar o inventário por nome, peso, raridade, valor mágico ou preço.
Complexidade:
```txt
O(n log n)
```

## Dados estilo RPG de mesa
O MVP agora usa dois testes simples com D20:
- **Dado de Mobilidade:** usado em viagens e ao avançar na Floresta Distorcida. A rolagem pode gerar atalho, perda de HP, recuperação de mana ou bônus de moedas.
- **Dado de Luta:** usado em ataques físicos, magias ofensivas de Henry, Quake/penas do Mitis e ataques dos mobs. A rolagem pode gerar falha crítica, golpe fraco, golpe normal, golpe forte ou crítico.
