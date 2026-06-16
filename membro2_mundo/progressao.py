"""Membro 2 — Progressão de nível, EXP e habilidades.

Regras do MVP:
- Matar criaturas gera EXP para o nível do Henry.
- Subir de nível aumenta status base por porcentagem equilibrada.
- As skills/magias evoluem por proficiência: uso direto e EXP de habilidade recebida em combate.
- Exemplo: usar Fire 10 vezes evolui Fire 0 -> Fire I.
- O ataque físico do Mitis é a Pena Envenenada, que também possui proficiência própria.
"""
from __future__ import annotations

# Cada família possui subníveis antes de trocar para a próxima magia.
# Exemplo: Fire -> Fire I -> Fire II -> Fire III -> Fira -> Fira I...
def _criar_tiers(base_names: list[str]) -> list[str]:
    tiers: list[str] = []
    for nome in base_names:
        tiers.extend([nome, f"{nome} I", f"{nome} II", f"{nome} III"])
    return tiers


FAMILIAS_MAGIAS = {
    # Henry
    "fire": _criar_tiers(["Fire", "Fira", "Firaga", "Firaja"]),
    "blizzard": _criar_tiers(["Blizzard", "Blizzara", "Blizzaga", "Blizzaja"]),
    "thunder": _criar_tiers(["Thunder", "Thundara", "Thundaga", "Thundaja"]),
    "water": _criar_tiers(["Water", "Watera", "Waterga", "Waterja"]),
    "dark": _criar_tiers(["Dark", "Darkra", "Darkga", "Darkja"]),

    # Mitis
    "mitis_penas": _criar_tiers(["Pena Envenenada", "Pena Venenosa", "Chuva de Penas", "Tempestade de Penas"]),
    "quake": _criar_tiers(["Quake", "Quakera", "Quakega", "Quakeja"]),
    "cure": _criar_tiers(["Cure", "Cura", "Curaga", "Curaja"]),
    "esuna": _criar_tiers(["Esuna", "Esunaga"]),
    "haste": _criar_tiers(["Haste", "Hastera", "Hastega"]),
    "protect": _criar_tiers(["Protect", "Protectga"]),
    "shell": _criar_tiers(["Shell", "Shellga"]),
}

HABILIDADES_VALIDAS = {
    "fire": "Henry usa magia de fogo: Fire -> Fira -> Firaga -> Firaja.",
    "blizzard": "Henry usa magia de gelo: Blizzard -> Blizzara -> Blizzaga -> Blizzaja.",
    "thunder": "Henry usa magia de trovão: Thunder -> Thundara -> Thundaga -> Thundaja.",
    "water": "Henry usa magia de água: Water -> Watera -> Waterga -> Waterja.",
    "dark": "Henry usa magia de escuridão: Dark -> Darkra -> Darkga -> Darkja.",
    "quake": "Mitis usa magia de terra: Quake -> Quakera -> Quakega -> Quakeja.",
    "cure": "Mitis usa cura: Cure -> Cura -> Curaga -> Curaja.",
    "esuna": "Mitis remove status negativos: Esuna -> Esunaga.",
    "haste": "Mitis acelera Henry: Haste -> Hastera -> Hastega.",
    "protect": "Mitis reduz dano físico recebido: Protect -> Protectga.",
    "shell": "Mitis reduz dano mágico/elemental recebido: Shell -> Shellga.",
    "mitis_penas": "Ataque físico do Mitis: Pena Envenenada. Evolui por proficiência de uso e aplica veneno.",
    "defesa": "Aumenta a resistência geral do grupo contra dano recebido.",
}

GRUPOS_HABILIDADES = {
    "Henry — Magias elementais": ["fire", "blizzard", "thunder", "water", "dark"],
    "Mitis — Ataque físico": ["mitis_penas"],
    "Mitis — Terra, cura e suporte": ["quake", "cure", "esuna", "haste", "protect", "shell"],
    "Defesa do grupo": ["defesa"],
}


def _max_nivel(chave: str) -> int:
    familia = FAMILIAS_MAGIAS.get(chave)
    if familia:
        return len(familia) - 1
    # Skills sem família de nomes ainda podem evoluir.
    return 15


def usos_para_proximo_nivel(chave: str, nivel: int) -> int:
    """Quantidade de usos necessária para evoluir por prática.

    A primeira evolução custa 10 usos, então:
    Fire 0 + 10 usos -> Fire I.
    Depois fica um pouco mais exigente para não evoluir rápido demais.
    """
    return 10 + (nivel * 5)


def exp_para_proximo_nivel_habilidade(chave: str, nivel: int) -> int:
    """EXP de habilidade necessária para evoluir por combate."""
    return 30 + (nivel * 15)


def nome_magia(chave: str, nivel: int) -> str:
    """Retorna o nome da magia conforme o nível de domínio."""
    familia = FAMILIAS_MAGIAS.get(chave)
    if not familia:
        return chave
    indice = min(max(nivel, 0), len(familia) - 1)
    return familia[indice]


def proximo_nome_magia(chave: str, nivel: int) -> str:
    familia = FAMILIAS_MAGIAS.get(chave)
    if not familia:
        return chave
    indice = min(nivel + 1, len(familia) - 1)
    return familia[indice]


def calcular_status_total(estado: dict) -> dict:
    """Soma status base + bônus de equipamentos."""
    total = estado["status"].copy()
    for item in estado.get("equipamentos", {}).values():
        if not item:
            continue
        for atributo, valor in item.get("efeitos", {}).items():
            if atributo in total:
                total[atributo] += valor
    return total


def garantir_estado_magias(estado: dict) -> None:
    """Garante compatibilidade caso um save antigo seja carregado."""
    habilidades = estado.setdefault("habilidades", {})
    for chave in HABILIDADES_VALIDAS:
        habilidades.setdefault(chave, 0)

    estado.setdefault("habilidade_usos", {})
    estado.setdefault("habilidade_exp", {})
    for chave in HABILIDADES_VALIDAS:
        estado["habilidade_usos"].setdefault(chave, 0)
        estado["habilidade_exp"].setdefault(chave, 0)

    status = estado.setdefault("status", {})
    for chave in ["fire", "blizzard", "thunder", "water", "dark", "quake", "cure", "esuna", "haste", "protect", "shell", "veneno"]:
        status.setdefault(chave, 0)
    status.setdefault("skill_points", 0)

    estado.setdefault("efeitos_temporarios", {})
    estado["efeitos_temporarios"].setdefault("haste", 0)
    estado["efeitos_temporarios"].setdefault("protect", 0)
    estado["efeitos_temporarios"].setdefault("shell", 0)
    estado["efeitos_temporarios"].setdefault("veneno", 0)
    estado["efeitos_temporarios"].setdefault("guarana_turnos", 0)
    estado["efeitos_temporarios"].setdefault("guarana_hp", 0)
    estado["efeitos_temporarios"].setdefault("guarana_mana", 0)


def _subir_nivel_habilidade(estado: dict, chave: str) -> bool:
    garantir_estado_magias(estado)
    nivel = estado["habilidades"].get(chave, 0)
    if nivel >= _max_nivel(chave):
        return False

    antigo = nome_magia(chave, nivel)
    estado["habilidades"][chave] = nivel + 1
    novo = nome_magia(chave, nivel + 1)
    print(f"\n*** SKILL UP! {chave} evoluiu: {antigo} -> {novo} ***")
    return True


def registrar_uso_habilidade(estado: dict, chave: str, quantidade: int = 1) -> None:
    """Registra uso prático de uma skill/magia.

    Exemplo: ao usar Fire em combate, soma +1 uso em fire.
    Quando chegar na quantidade necessária, a magia evolui.
    """
    garantir_estado_magias(estado)
    if chave not in HABILIDADES_VALIDAS:
        return

    if estado["habilidades"].get(chave, 0) >= _max_nivel(chave):
        return

    estado["habilidade_usos"][chave] += quantidade

    while estado["habilidades"].get(chave, 0) < _max_nivel(chave):
        nivel = estado["habilidades"].get(chave, 0)
        necessario = usos_para_proximo_nivel(chave, nivel)
        if estado["habilidade_usos"][chave] < necessario:
            break
        estado["habilidade_usos"][chave] -= necessario
        _subir_nivel_habilidade(estado, chave)


def ganhar_exp_habilidade(estado: dict, chave: str, quantidade: int) -> None:
    """Adiciona EXP própria para a habilidade usada no combate."""
    garantir_estado_magias(estado)
    if chave not in HABILIDADES_VALIDAS or quantidade <= 0:
        return

    if estado["habilidades"].get(chave, 0) >= _max_nivel(chave):
        return

    estado["habilidade_exp"][chave] += quantidade
    print(f"{chave} recebeu {quantidade} EXP de habilidade.")

    while estado["habilidades"].get(chave, 0) < _max_nivel(chave):
        nivel = estado["habilidades"].get(chave, 0)
        necessario = exp_para_proximo_nivel_habilidade(chave, nivel)
        if estado["habilidade_exp"][chave] < necessario:
            break
        estado["habilidade_exp"][chave] -= necessario
        _subir_nivel_habilidade(estado, chave)


def ganhar_exp_habilidades_usadas(estado: dict, habilidades_usadas: list[str], exp_inimigo: int) -> None:
    """Distribui parte da EXP do mob entre as skills usadas na luta.

    Assim a skill progride tanto pelo uso direto quanto pela recompensa do mob.
    """
    garantir_estado_magias(estado)
    unicas = []
    for chave in habilidades_usadas:
        if chave in HABILIDADES_VALIDAS and chave not in unicas:
            unicas.append(chave)
    if not unicas:
        return

    exp_por_skill = max(1, int((exp_inimigo * 0.25) / len(unicas)))
    print("\nEXP de habilidade pelas ações usadas na batalha:")
    for chave in unicas:
        ganhar_exp_habilidade(estado, chave, exp_por_skill)


def ganhar_exp(estado: dict, quantidade: int) -> None:
    garantir_estado_magias(estado)
    status = estado["status"]
    status["exp"] += quantidade
    print(f"Henry ganhou {quantidade} EXP.")

    while status["exp"] >= status["exp_proximo"]:
        status["exp"] -= status["exp_proximo"]
        subir_nivel(estado)


def subir_nivel(estado: dict) -> None:
    garantir_estado_magias(estado)
    status = estado["status"]
    status["nivel"] += 1

    status["hp_max"] = int(status["hp_max"] * 1.10)
    status["mana_max"] = int(status["mana_max"] * 1.08)
    status["ataque"] = int(status["ataque"] * 1.07) + 1
    status["defesa"] = int(status["defesa"] * 1.06) + 1
    status["magia"] = int(status["magia"] * 1.08) + 1

    status_total = calcular_status_total(estado)
    status["hp"] = status_total["hp_max"]
    status["mana"] = status_total["mana_max"]
    status["exp_proximo"] = int(status["exp_proximo"] * 1.35)

    # Mantido por compatibilidade, mas a progressão principal de skills agora é por uso/EXP de habilidade.
    status["skill_points"] += 1

    print("\n*** LEVEL UP! ***")
    print(f"Henry chegou ao nível {status['nivel']}.")
    print("Status base aumentaram de forma equilibrada.")
    print("As magias continuam evoluindo principalmente por uso e EXP de habilidade.")


def _texto_progresso_skill(estado: dict, chave: str) -> str:
    nivel = estado["habilidades"].get(chave, 0)
    if nivel >= _max_nivel(chave):
        return "MAX"
    usos = estado["habilidade_usos"].get(chave, 0)
    exp_skill = estado["habilidade_exp"].get(chave, 0)
    return (
        f"usos {usos}/{usos_para_proximo_nivel(chave, nivel)} | "
        f"skill EXP {exp_skill}/{exp_para_proximo_nivel_habilidade(chave, nivel)}"
    )


def mostrar_status(estado: dict) -> None:
    garantir_estado_magias(estado)
    status_total = calcular_status_total(estado)
    base = estado["status"]
    print("\n=== STATUS DE HENRY E MITIS ===")
    print(f"Jogador: {estado['jogador']}")
    print(f"Companheiro: {estado['companheiro']}")
    print(f"Nível: {base['nivel']} | EXP: {base['exp']}/{base['exp_proximo']}")
    print(f"HP: {base['hp']}/{status_total['hp_max']}")
    print(f"Mana do grupo: {base['mana']}/{status_total['mana_max']}")
    print(f"Ataque físico: {status_total['ataque']}")
    print(f"Defesa: {status_total['defesa']}")
    print(f"Magia base: {status_total['magia']}")
    print(f"Moedas: {estado['moedas']}")

    print("\nBônus elementais/equipamentos:")
    for chave in ["fire", "blizzard", "thunder", "water", "dark", "quake", "cure", "haste", "protect", "shell", "veneno"]:
        print(f"- {chave}: {status_total.get(chave, 0)}")

    print("\nEfeitos temporários:")
    efeitos = estado.get("efeitos_temporarios", {})
    print(f"- Haste: {efeitos.get('haste', 0)} turno(s)")
    print(f"- Protect: {efeitos.get('protect', 0)} turno(s)")
    print(f"- Shell: {efeitos.get('shell', 0)} turno(s)")
    print(f"- Veneno em Henry: {efeitos.get('veneno', 0)} turno(s)")
    print(f"- Guaraná: {efeitos.get('guarana_turnos', 0)} turno(s) | +{efeitos.get('guarana_hp', 0)} HP / +{efeitos.get('guarana_mana', 0)} mana por turno")

    print("\n=== PROFICIÊNCIA DE SKILLS ===")
    print("As magias evoluem por uso direto ou EXP de habilidade recebida ao vencer mobs.")
    print("Exemplo: Fire 0 + 10 usos -> Fire I.")
    for grupo, nomes in GRUPOS_HABILIDADES.items():
        print(f"\n{grupo}:")
        for chave in nomes:
            nivel = estado["habilidades"].get(chave, 0)
            atual = nome_magia(chave, nivel)
            prox = proximo_nome_magia(chave, nivel)
            progresso = _texto_progresso_skill(estado, chave)
            print(f"- {chave}: nível {nivel} | atual: {atual} | próximo: {prox} | {progresso}")


def gastar_ponto_habilidade(estado: dict) -> None:
    """Tela de treinamento manual opcional.

    A progressão principal agora é por uso/EXP. Esta função fica como treino extra
    caso o jogador tenha ponto sobrando por level up.
    """
    garantir_estado_magias(estado)
    if estado["status"].get("skill_points", 0) <= 0:
        print("Henry não possui pontos de treino disponíveis.")
        print("Use magias em combate ou vença mobs para evoluir habilidades.")
        return

    print("\n=== TREINAR HABILIDADE ===")
    print("A progressão principal é por uso/EXP, mas pontos de treino podem adiantar uma skill.")
    opcoes: list[str] = []
    for grupo, nomes in GRUPOS_HABILIDADES.items():
        print(f"\n{grupo}:")
        for nome in nomes:
            opcoes.append(nome)
            idx = len(opcoes)
            nivel = estado["habilidades"].get(nome, 0)
            atual = nome_magia(nome, nivel)
            prox = proximo_nome_magia(nome, nivel)
            print(f"{idx} - {nome} | nível {nivel} | atual: {atual} | próximo: {prox}")
    print("0 - Cancelar")

    escolha = input("Escolha o número da habilidade: ").strip()
    if escolha == "0":
        print("Treino cancelado.")
        return
    if not escolha.isdigit() or not 1 <= int(escolha) <= len(opcoes):
        print("Opção inválida.")
        return

    chave = opcoes[int(escolha) - 1]
    if _subir_nivel_habilidade(estado, chave):
        estado["status"]["skill_points"] -= 1
    else:
        print("Essa habilidade já está no nível máximo.")
