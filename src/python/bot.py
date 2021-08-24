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
def main(diretorioBase):
    print("########################################################################")
    print("#                Bem vindo ao Gerador de Projetos                      #")
    print("#                            Versão 2.0                                #")
    print("#                                                                      #")
    print("# Requisitos Básicos:                                                  #")
    print("#    - NetCore SDK 5                                                   #")
    print("#    - NodeJS                                                          #")
    print("#         - Angular CLI                                                #")
    print("#         - VueJS CLI                                                  #")
    print("#    - Git                                                             #")
    print("#                                                                      #")
    print("#                                                                      #")
    print("########################################################################")  
    print(" ")  
    print(" ")  

    acao = input('''Deseja criar ou atualizar um projeto?
    ( 1 ) Criar Projeto [Dominio Unico]
    ( 2 ) Criar Projeto [Dominios Multiplos]
    ( 3 ) Atualizar Projeto
    Escolha: ''')

    #Verificando qual ação será tomada 
    #Atualizar projeto ou gerar um novo
    if acao == '1' or acao == '2': 
        novo_projeto.gerarNovoProjeto(diretorioBase, acao, 'true')
    
    if acao == '3':
        atualiza_projeto.atualizarProjeto()         
    
    print("Processo Finalizado")
main(diretorioBase)
