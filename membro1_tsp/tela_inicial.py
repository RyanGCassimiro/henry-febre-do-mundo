"""Tela inicial textual do jogo.

Responsável: Membro 1 (Wanessa):
Função:
- Exibir o nome do jogo;
- Apresentar o menu inicial;
- Permitir iniciar novo jogo, carregar jogo, ver créditos ou sair.
"""

from __future__ import annotations


def mostrar_titulo() -> None:
    """Mostra o título do jogo no terminal."""
    print("\n" + "=" * 72)
    print("HENRY E A FLORESTA DO MUNDO".center(72))
    print("=" * 72)
    print("Um RPG de mesa em terminal sobre rotas, magia e uma floresta viva.".center(72))
    print("-" * 72)
    print("Henry viaja com Mitis, a corujinha-buraqueira, para investigar")
    print("a febre mágica que distorce a Árvore do Mundo e seus caminhos.")
    print("=" * 72)


def menu_tela_inicial() -> str:
    """Exibe a tela inicial e retorna a escolha do jogador."""
    while True:
        mostrar_titulo()
        print("\nMENU INICIAL")
        print("1 - Novo jogo")
        print("2 - Carregar")
        print("3 - Créditos")
        print("0 - Sair")

        opcao = input("\nEscolha: ").strip()

        if opcao in {"1", "2", "3", "0"}:
            return opcao

        print("\nOpção inválida. Escolha 1, 2, 3 ou 0.")
        input("Pressione ENTER para tentar novamente...")
