import cmd
import textwrap
import sys
import os
import time
import random
from utilitarios import(
    limpar_tela
)

######### Setup do jogador ########

class Player:
    def __init__(self):
        self.nome = ''
        self.classe = ''
        self.nivel = 1
        self.vida = 0
        self.vida_max = self.vida
        self.mana = 0
        self.mana_max = self.mana
        self.atk = 5
        self.efeitos_status = []
        self.local = 'começo'
        self.game_over = False

class Monstro:
    def __init__(self):
        self.nome = 'slime'
        self.vida = 10
        self.vida_max = self.vida
        self.nivel = 1
        self.atk = 2
        self.xp = 20

monstro_exemplo = Monstro()
meu_jogador = Player()

######### Tela de título #########

def navegação_tela_titulo():
    opção = input(">").lower()
    while opção not in ['jogar', 'ajuda', 'sair']:
        print("Por favor, utilize um comando válido.")
        opção = input(">").lower()
    if opção == "jogar":
        setup_jogo()
    elif opção == "ajuda":
        ajuda_menu()
    elif opção == "sair":
        sys.exit()

def tela_titulo():
    limpar_tela()
    print('#########################')
    print('# >Bem vindo ao ARKYOS! #')
    print('#########################')
    print('        - Jogar -        ')
    print('        - Ajuda -        ')
    print('        - Sair  -        ')
    navegação_tela_titulo()

def ajuda_menu():
    limpar_tela()
    print('#########################')
    print('# >Bem vindo ao ARKYOS! #')
    print('#########################' "\n")
    print('- Digite mover para se movimentar')
    print('- Digite seus comandos para executá-los')
    print('- Use o comando "inspecionar ou olhar" para examinar algo')
    print('- Boa sorte e não morra :p')
    if meu_jogador.nome != '':
        print('Voltar ao game? [s/n]')
        voltar_game = input('>>').lower()
        if voltar_game != 's':
            limpar_tela()
            ajuda_menu()
        main_game_loop()
    print("voltar ao MENU? [s/n]")
    voltar_menu = input('>>').lower()
    if voltar_menu != 's':
        limpar_tela()
        ajuda_menu()
    tela_titulo()

#### Funções do jogo ####

def start_game():
    meu_jogador.local = 'a1'

#### Mapa #####

DESCRICAO = 'DESCRICAO'
EXAMINAR = 'EXAMINAR'
SOLVED = 'SOLVED'
CIMA = 'CIMA'
BAIXO = 'BAIXO'
ESQUERDA = 'ESQUERDA'
DIREITA = 'DIREITA'

lugares_resolvidos = {
    'a1': False, 'a2': False, 'a3': False, 'a4': False,
    'b1': False, 'b2': False, 'b3': False, 'b4': False,
    'c1': False, 'c2': False, 'c3': False, 'c4': False,
    'd1': False, 'd2': False, 'd3': False, 'd4': False,
}

mapa = {
    'a1': {
        'NOME_LOCAL': 'Sala 1',
        'DESCRICAO': 'Local de início, você começa aqui!',
        'EXAMINAR': 'Você vê duas galinhas.',
        'SOLVED': False,
        'CIMA': '',
        'BAIXO': '',
        'ESQUERDA': 'a2',
        'DIREITA': '',
        'MONSTRO': ''
    },
    'a2': {
        'NOME_LOCAL': "Sala2",
        'DESCRICAO': 'Descrição da sala 2.',
        'EXAMINAR': 'Você observa objetos antigos.',
        'SOLVED': False,
        'CIMA': '',
        'BAIXO': 'b1',
        'ESQUERDA': '',
        'DIREITA': 'a1',
        'MONSTRO': monstro_exemplo
    },
    'b1': {
        'NOME_LOCAL': "Sala1 Segundo andar",
        'DESCRICAO': 'Descrição da sala b1.',
        'EXAMINAR': 'Uma escada quebrada e mobília velha.',
        'SOLVED': False,
        'CIMA': 'a2',
        'BAIXO': '',
        'ESQUERDA': 'b2',
        'DIREITA': '',
        'MONSTRO': ''
    },
    'b2': {
        'NOME_LOCAL': "Sala2 Segundo andar",
        'DESCRICAO': 'Descrição da sala b2.',
        'EXAMINAR': 'Rochas espalhadas pelo chão.',
        'SOLVED': False,
        'CIMA': '',
        'BAIXO': 'c1',
        'ESQUERDA': '',
        'DIREITA': 'b1',
        'MONSTRO': ''
    },
    'c1': {
        'NOME_LOCAL': "Sala1 Terceiro andar",
        'DESCRICAO': 'Descrição da sala c1.',
        'EXAMINAR': 'Velhas tapeçarias nas paredes.',
        'SOLVED': False,
        'CIMA': 'b2',
        'BAIXO': '',
        'ESQUERDA': 'c2',
        'DIREITA': '',
        'MONSTRO': ''
    },
    'c2': {
        'NOME_LOCAL': "Sala2 Terceiro andar",
        'DESCRICAO': 'Descrição da sala c2.',
        'EXAMINAR': 'Eco assustador.',
        'SOLVED': False,
        'CIMA': '',
        'BAIXO': '',
        'ESQUERDA': '',
        'DIREITA': 'c1',
        'MONSTRO': ''
    },
}

#mapa mental dos andares:
#|a1|a2|
#|b1|b2|
#|c2|c1|
#Começamos em a1

##### Interações em jogo #####

def print_local():
    local_nome = mapa[meu_jogador.local]['NOME_LOCAL']
    local_desc = mapa[meu_jogador.local]['DESCRICAO']
    print('\n' + ('#' * (4 + len(local_nome))))
    print(f"# {local_nome.upper()} #")
    print(f"# {local_desc} #")
    print('#' * (4 + len(local_nome)))
    if mapa[meu_jogador.local]['MONSTRO'] != '':
        print(f"há um {monstro_exemplo.nome} na sala. O que deseja fazer?\n[atacar / fugir / falar]")
        escolha = input(">>").lower()
        if escolha not in ['atacar', 'fugir', 'falar']:
            print_local()
        acao_luta(escolha, mapa[meu_jogador.local]['MONSTRO'])

def prompt():
    print("\n" + "=====================================")
    print("O que deseja fazer?")
    acao = input("-> ").lower()
    acoes_aceitas = ['examinar', 'mover', 'sair', 'ajuda', 'olhar', 'pegar', 'inspecionar', 'ir', 'usar', 'teleportar', 'dormir']
    while acao not in acoes_aceitas:
        print("Ação inválida, tente novamente.\n")
        acao = input("-> ").lower()
    if acao == 'sair':
        sys.exit()
    elif acao in ['mover', 'ir', 'teleportar']:
        jogador_mover()
    elif acao == 'ajuda':
        ajuda_menu()
    elif acao in ['examinar', 'olhar', 'inspecionar']:
        jogador_examinar()
    elif acao == 'pegar':
        jogador_pegar()
    elif acao == 'usar':
        jogador_usar()
    elif acao == 'dormir':
        jogador_dormir()

def acao_luta(escolha, monstro):
    if escolha == 'atacar':
        luta(monstro)
    elif escolha == 'fugir':
        if meu_jogador.local == 'a2':
            print('você voltou para a sala anterior')
            meu_jogador.local = 'a1'
        print_local()
    elif escolha == 'falar':
        print(f'O {monstro.nome} não te entende e te ataca')
        meu_jogador.vida -= monstro_exemplo.atk
        luta(monstro)


def luta(monstro):
    print(f'\n{monstro.nome} #{monstro.nivel}')
    print(f'vida: {monstro.vida}/{monstro.vida_max} ATK: {monstro.atk}')
    print('-'*50)
    print(f'{meu_jogador.nome} #{meu_jogador.nivel}')
    print(f'vida: {meu_jogador.vida}/{meu_jogador.vida_max} ATK: {meu_jogador.atk}')
    print('atacar / magia / fugir')
    acao = input(">>").lower()
    if acao not in ['atacar', 'magia', 'fugir']:
        limpar_tela()
        print("comando invádido".upper())
        luta(monstro)
    if acao == 'atacar':
        monstro.vida -= meu_jogador.atk
        print(f"você ataca {monstro.nome}\n")
        for i in range(0, 5):
            sys.stdout.write('. ')
            sys.stdout.flush()
            time.sleep(0.2)
        time.sleep(0.3)

        meu_jogador.vida -= monstro.atk
        if monstro.vida > 0:
            print(f'\no {monstro.nome} te ataca\n')
            for i in range(0, 5):
                sys.stdout.write('. ')
                sys.stdout.flush()
                time.sleep(0.2)
        time.sleep(0.3)
        if meu_jogador.vida > 0 and monstro.vida > 0:
            luta(monstro)
        
        if meu_jogador.vida <= 0:
            meu_jogador.local = 'a1'
            meu_jogador.vida = meu_jogador.vida_max
            limpar_tela()
            print('Você morreu e acorda na sala inicial')
        elif monstro.vida <= 0:
            limpar_tela()
            print(f'VOCÊ DERROTOU {monstro.nome}')
            mapa[meu_jogador.local]['MONSTRO'] = ''
            print_local()
    elif acao == 'magia':
        print('Você ainda não sabe magias')
        for i in range(0, 5):
            sys.stdout.write('. ')
            sys.stdout.flush()
            time.sleep(0.2)
        print(f'o {monstro.nome}')


def jogador_dormir():
    print("Dormindo...")

def jogador_mover():
    pergunta = "Para onde deseja se mover? (cima, baixo, esquerda, direita)\n"
    dest = input(pergunta).lower()
    direcoes_validas = ['cima', 'baixo', 'esquerda', 'direita']
    if dest in direcoes_validas:
        destino = mapa[meu_jogador.local][dest.upper()]
        if destino:
            movimento_manipulado(destino)
        else:
            print("Você não pode se mover nessa direção.")
    else:
        print("Direção inválida.")

def jogador_usar():
    print("Você usou um item, mas essa função ainda será detalhada.")

def jogador_pegar():
    print("Você pegou um item, mas essa função ainda será detalhada.")

def movimento_manipulado(destino):
    print(f"\nVocê se moveu para {destino}.")
    meu_jogador.local = destino
    print_local()

def jogador_examinar():
    if mapa[meu_jogador.local]['SOLVED']:
        print("Você já examinou aqui.")
    else:
        print(mapa[meu_jogador.local]['EXAMINAR'])
        mapa[meu_jogador.local]['SOLVED'] = True

##### Fluxo principal #####

def main_game_loop():
    while not meu_jogador.game_over:
        prompt()
        # Aqui tratar se os enigmas foram resolvidos, chefe derrotado, tudo explorado, etc.

def setup_jogo():
    os.system('clear' if os.name != 'nt' else 'cls')

    pergunta1 = "\n Qual seu nome?\n"
    for caractere in pergunta1:
        sys.stdout.write(caractere)
        sys.stdout.flush()
        time.sleep(0.04)
    meu_jogador.nome = input("-> ")

    pergunta2 = "Qual sua classe?\n(Escolha: guerreiro, mago ou despojado)\n"
    for caractere in pergunta2:
        sys.stdout.write(caractere)
        sys.stdout.flush()
        time.sleep(0.04)

    classes_validas = ['guerreiro', 'mago', 'despojado']
    jogador_classe = input("-> ").lower()
    while jogador_classe not in classes_validas:
        print("Classe inválida, tente novamente.")
        jogador_classe = input("-> ").lower()
    meu_jogador.classe = jogador_classe
    print(f"Classe selecionada: {meu_jogador.classe.capitalize()}\n")

    if meu_jogador.classe == 'guerreiro':
        meu_jogador.vida = 120
        meu_jogador.vida_max = meu_jogador.vida
        meu_jogador.mana = 20
    elif meu_jogador.classe == 'mago':
        meu_jogador.vida = 40
        meu_jogador.vida_max = meu_jogador.vida
        meu_jogador.mana = 120
    elif meu_jogador.classe == 'despojado':
        meu_jogador.vida = 60
        meu_jogador.vida_max = meu_jogador.vida
        meu_jogador.mana = 60

    fala1 = f"Bem-vindo, {meu_jogador.nome} o {meu_jogador.classe.capitalize()}!\n"
    fala2 = "Espero que se divirta nessa incrível aventura!\n"
    fala3 = "Seu objetivo é descer a Torre de ARKYOS vivo, mas cuidado com os monstros que espreitam por aqui. Boa sorte!\n"

    for fala in [fala1, fala2, fala3]:
        for caractere in fala:
            sys.stdout.write(caractere)
            sys.stdout.flush()
            time.sleep(0.03)
    time.sleep(2)

    os.system('clear' if os.name != 'nt' else 'cls')
    print ("=====================================")
    introducao1 = f'nome: {meu_jogador.nome} // classe: {meu_jogador.classe} // vida: {meu_jogador.vida} // mana: {meu_jogador.mana} \n'
    for introducao in introducao1:
        sys.stdout.write(introducao)
        sys.stdout.flush()
        time.sleep(0.02)
    introducao2 = 'Você acordou naquele quarto escuro, aparentemente sua luz acabou e você não sabe o por que. \n Você vivia pacificamente em seu quarto e nunca precisou sair pois um cara sempre trazia tudo que você precisa mas aparentemente essa pessoa sumiu.\n Agora é com você o encontrar.\n'
    for introducao in introducao2:
        sys.stdout.write(introducao)
        sys.stdout.flush()
        time.sleep(0.01)
    ajuda = 'Lista de comandos: (examinar, mover, sair, ajuda, pegar, usar, ir, teleportar, dormir)\n'
    for ajuda in ajuda:
        sys.stdout.write(ajuda)
        sys.stdout.flush()
        time.sleep(0.01)

    start_game()
    main_game_loop()

##### Executar #####
tela_titulo()