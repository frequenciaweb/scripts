'''
Bot Gerador de Projetos.
Este bot foi desenvolvido em python para fins de estudo na linguagem e para gerar projetos dot net e configuralos com padrões de projetos
e arquiteturas de softwares diversas gerando tambem alguns códigos afim de deixar o
desenvolvimento mais rapido
'''
import os
import sys

import novo_projeto
import atualiza_projeto

os.system('cls' if os.name == 'nt' else 'clear')

diretorioBase = os.getcwd()
print("Diretório base: "+diretorioBase) 

def main(diretorioBase):
    print('''Bem vindo ao Gerador de Projetos 2.0
    Requisitos Básicos:
    - NetCore SDK 5
    - NodeJS
    - NPM
        - Angular CLI
        - VueJS CLI
    - Git''')

    acao = input('''Deseja criar ou atualizar um projeto?
    ( 1 ) Criar Projeto
    ( 2 ) Atualizar Projeto
    Escolha: ''')

    #Verificando qual ação será tomada 
    #Atualizar projeto ou gerar um novo
    if acao == '1': 
        novo_projeto.gerarNovoProjeto('true', diretorioBase)
    
    if acao == '2':
        atualiza_projeto.atualizarProjeto()         
    
    print("Processo Finalizado")
main(diretorioBase)
