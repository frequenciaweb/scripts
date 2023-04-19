import os
import sys


class Diretorio(object):
    @staticmethod
    def mudar(caminho):
        atual = os.getcwd()
        if (atual != caminho):
            print('Mudando Diretório de: '+atual+' para: '+caminho)
            os.chdir(caminho)

    def criarComArquivoExemplo(caminho, arquivo_txt):        
        print('Criando Diretorio: '+caminho)        
        os.makedirs(caminho)        
        os.system("echo # "+arquivo_txt+" >> "+caminho+"\\leiame.txt");
        
    def criar(caminho):        
        print('Criando Diretorio: '+caminho)        
        os.makedirs(caminho)        
