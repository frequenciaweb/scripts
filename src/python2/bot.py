
'''
Bot Gerador de Projetos.
Este bot foi desenvolvido em python para fins de estudo na linguagem e para gerar projetos dot net e configuralos com padrões de projetos
e arquiteturas de softwares diversas gerando tambem alguns códigos afim de deixar o
desenvolvimento mais rapido
'''
import os
import sys
from core.nucleo import Nucleo
from core.solucao import Solucao


class Bot(Nucleo):
    
    def __init__(self):     
        super().__init__()
        print("########################################################################")
        print("#                Bem vindo ao Gerador de Projetos                      #")
        print("#                            Versão 2.2                                #")
        print("#                                                                      #")
        print("# Requisitos Básicos:                                                  #")
        print("#    - NetCore SDK                                                     #")
        print("#    - NodeJS                                                          #")
        print("#         - Angular CLI                                                #")
        print("#         - VueJS CLI                                                  #")
        print("#         - NPM                                                        #")
        print("#    - Git                                                             #")
        print("#                                                                      #")
        print("#                                                                      #")
        print("########################################################################")  
        print(" ")  
        print(" ")  
        
    def executarTeste(self):
        print('Executar Teste')  
        return Solucao("ProjetoTeste","D:\Projetos","frequenciaweb",1)
            
    def coletarInformacoesDoProjeto(self):
        print('Coletar informações do projeto')    
        
    def iniciar(self, debug = 'false'):   
        if debug == 'false': 
          projeto = self.coletarInformacoesDoProjeto()
        else:
          projeto = self.executarTeste()
          
        self.gerarSolucao(projeto)  

bot = Bot()
bot.iniciar('true')