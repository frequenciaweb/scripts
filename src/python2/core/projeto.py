from ast import Return
import os
import sys
import pandas as pd
import json
from json import JSONEncoder

class Projeto():
    def __init__(self, nome,  solucao, pasta, cli, packages=[], references=[], folders=[], templates=[]):       
        self.nome = nome
        pasta = pasta.replace("%nameSolution%", solucao)
        self.cli = cli.replace("%nameSolution%", solucao) + " --output="+pasta
        # identificar se o comando é dotnet ou npm
        self.dotnet = cli.index("dotnet") >= 0
        self.projeto = self.nome+".cs"
        self.caminho = pasta
        self.references = references
        self.packages = packages
        self.folders = folders
        self.templates = templates    
        if (cli == 'angular'):
            self.cli = "ng new "+nome
            self.projeto = ""
            self.caminho = pasta+"\\"+self.nome
        if (cli == 'vue'):
            self.cli = "vue create "+nome
            self.projeto = ""
            self.caminho = pasta+"\\"+self.nome
            
    def mudarDiretorio(self, caminho):
        print("saindo de "+os.getcwd()+" para "+caminho)
        os.chdir(caminho)



    def dotNet(self):
        print('Instalando pacotes')
        for pk in self.packages:
            os.system("dotnet add package "+pk)

        print('Criando pastas')
        if (self.dotnet):
            for fd in self.folders:
                os.makedirs(fd)



    def gerar(self):
        print('Gerando projeto '+self.nome)
        os.makedirs(self.caminho)
        if (self.cli == 'angular'):
            # mudando para o diretorio onde ficara o projeto
            self.mudarDiretorio(self.caminho)
            
            os.system(self.cli)
            os.system("ng build")

        if (self.cli == 'vue'):
            # mudando para o diretorio onde ficara o projeto
            self.mudarDiretorio(self.caminho)
            os.system("npm run build")

        if (self.cli != 'vue' and self.cli != 'angular'):
            os.system(self.cli)
            # mudando para o diretorio onde ficara o projeto
            self.mudarDiretorio(self.caminho)

        if (self.dotnet):
            self.dotNet()

        if (self.dotnet == 'false'):
            for pk in self.packages:
                os.system("npm install -g "+pk)    