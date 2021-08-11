"""
Bot Gerador de Projetos.
Este bot foi desenvolvido em python para fins de estudo na linguagem e para gerar projetos dot net e configuralos com padrões de projetos
e arquiteturas de softwares diversas gerando tambem alguns códigos afim de deixar o
desenvolvimento mais rapido
"""

import os
import sys

import src.novo_projeto
import src.atualiza_projeto

os.system('cls' if os.name == 'nt' else 'clear')

def main():
    print("Bem vindo ao Gerador de Projetos 2.0 \n"
"Requisitos Basicos \n"
"- NetCore SDK \n"
"- NodeJS \n"
"   - NPM \n"
"       - Pacote Angular \n"
"       - Pacote VueJS \n"
"- Git")

    acao = input("Deseja criar um novo projeto ou atualizar um existente? \n"
    "( 1 ) Novo Projeto \n"
    "( 2 ) Atualizar Projeto \n"
    "Escolha: ")

    if acao == '1': 
        src.novo_projeto.gerarNovoProjeto()
    
    if acao == '2':
        src.atualiza_projeto.atualizarProjeto()         
    
    print("Processo Finalizado")
main()