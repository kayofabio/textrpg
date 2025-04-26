import cmd
import textwrap
import sys
import os
import time
import random

class Player:
    def __init__(self):
        self.nome = ''
        self.classe = ''
        self.vida = 0
        self.mana = 0
        self.dano_base = 5
        self.efeitos_status = []
        self.local = 'começo'
        self.game_over = False  
        self.inventario = {}   
        self.equipamento = None 

meu_jogador = Player()

itens = ['poção de vida', 'espada de ferro', 'arco longo', 'poção de mana']
itens_dano = ['espada de ferro', 'arco longo']

def adicionar_item(item, quantidade):
    if item in meu_jogador.inventario: 
        meu_jogador.inventario[item] += quantidade
    else:
        meu_jogador.inventario[item] = quantidade

def remover_item(item, quantidade):
    if item in meu_jogador.inventario:
        meu_jogador.inventario[item] -= quantidade
        if meu_jogador.inventario[item] <= 0:
            del meu_jogador.inventario[item]
    else:
        print("Item inexistente no inventário.")

def mostrar_inventario():
    print(
        f"""
 _____                             _                 _        
|_   _|                           | |               (_)       
  | |   _ __  __   __  ___  _ __  | |_   __ _  _ __  _   ___  
  | |  | '_ \ \ \ / / / _ \| '_ \ | __| / _` || '__|| | / _ \ 
 _| |_ | | | | \ V / |  __/| | | || |_ | (_| || |   | || (_) |
 \___/ |_| |_|  \_/   \___||_| |_| \__| \__,_||_|   |_| \___/ 
                      
                     Dano atual: {calcular_dano()}
                                                              
"""
    )
    for item, quantidade in meu_jogador.inventario.items():
        print(f'> {item} x{quantidade}')
    print()

def equipar_item(item):
    if item in meu_jogador.inventario:
        if item in itens_dano:
            if meu_jogador.equipamento:
                print(f'Você desequipou {meu_jogador.equipamento["nome"]}.')  # Mensagem de desequipar
            if item == 'espada de ferro':
                meu_jogador.equipamento = {
                    'nome': 'espada de ferro',
                    'bonus_dano': 15
                }
                print('Você equipou a espada de ferro! (+15 de dano)')
            elif item == 'arco longo':
                meu_jogador.equipamento = {
                    'nome': 'arco longo',
                    'bonus_dano': 20
                }
                print('Você equipou o arco longo! (+20 de dano)')
        else:
            print('Esse item não pode ser equipado.')
    else:
        print('Item inexistente no inventário.')

def calcular_dano():
    dano_total = meu_jogador.dano_base
    if meu_jogador.equipamento:
        dano_total += meu_jogador.equipamento['bonus_dano']
    return dano_total
    
print('Você anda pela rua e vê uma espada no chão, ela parece ser uma espada de ferro, deseja pega-la?')
print('1. Sim\n2. Nao')
resposta = input('-> ')
if resposta == '1':
    adicionar_item('espada de ferro', 1)
    print('Voce pegou a espada de ferro!!! deseja equipar-la?')
    print('1. Sim\n2. Nao')
    resposta = input('-> ')
    if resposta == '1':
        equipar_item('espada de ferro')
    else:
        print("A espada foi guardada no seu inventario.")
else:
    print('Ok, vamos continuar.')

print('deseja ver seu inventario?')
print('1. Sim\n2. Nao')
resposta = input('-> ')
if resposta == '1':
    mostrar_inventario()
else:
    print('Ok, vamos continuar.')