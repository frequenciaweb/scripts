'''
Bot Gerador de Projetos.
Este bot foi desenvolvido em python para fins de estudo na linguagem e para gerar projetos dot net e configuralos com padrões de projetos
e arquiteturas de softwares diversas gerando tambem alguns códigos afim de deixar o
desenvolvimento mais rapido
'''
import os
import sys

import src.novo_projeto
import src.atualiza_projeto

os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print('''Bem vindo ao Gerador de Projetos 2.0
    Requisitos Básicos:
    - NetCore SDK
    - NodeJS
    - NPM
        - Angular CLI
        - VueJS CLI
    - Git''')

    acao = input('''\nDeseja criar ou atualizar um projeto?
    ( 1 ) Criar Projeto
    ( 2 ) Atualizar Projeto
    Escolha: ''')

    if acao == '1': 
        src.novo_projeto.gerarNovoProjeto()
    
    if acao == '2':
        src.atualiza_projeto.atualizarProjeto()         
    
    print("Processo Finalizado")
main()
