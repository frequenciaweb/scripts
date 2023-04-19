from ast import Return
import os
import sys
import pandas as pd
import json
from json import JSONEncoder
from models.template import Template
from leitor_json import retornarArquivoTemplate

from funcoes import filtroProjeto


class ConfiguracaoProjeto:
    def __init__(self, identificador, solucao, pasta, cli, packages=[], references=[], folders=[], templates=[]):
        self.identificador = identificador
        self.nome = solucao
        pasta = pasta.replace("%nameSolution%", solucao)
        self.cli = cli.replace("%nameSolution%", solucao) + " --output="+pasta
        # identificar se o comando é dotnet ou npm
        self.dotnet = cli.index("dotnet") >= 0
        self.projeto = self.nome+"."+identificador+".cs"
        self.caminho = pasta
        self.references = references
        self.packages = packages
        self.folders = folders
        self.templates = templates

        if (cli == 'angular'):
            self.cli = "ng new "+identificador
            self.projeto = ""
            self.caminho = pasta+"\\"+self.nome
        if (cli == 'vue'):
            self.cli = "vue create "+identificador
            self.projeto = ""
            self.caminho = pasta+"\\"+self.nome

    def mudarDiretorio(self, caminho):
        print("saindo de "+os.getcwd()+" para "+caminho)
        os.chdir(caminho)

    def GerarTemplates(self, diretorioBase):
        print('Gerando Templates')

        for t in self.templates:
            template = retornarArquivoTemplate(t['name'], diretorioBase)
            if template == "":
                print('Template não encontrado '+t['name'])
                return

            cwd = os.getcwd()

            a = cwd+'\\'+t['file']
            if t['folder'] != "":
                a = cwd+'\\'+t['folder']+'\\'+t['file']

            arquivo = open(a, 'w')
            for linha in template:
                novo = linha.replace("%solution%", self.nome)
                novo = novo.replace("%projectName%", self.identificador)
                arquivo.write(novo)
            arquivo.close()

    def dotNet(self):
        print('Instalando pacotes')
        for pk in self.packages:
            os.system("dotnet add package "+pk)

        print('Criando pastas')
        if (self.dotnet):
            for fd in self.folders:
                os.makedirs(fd)

    def referenciar(self, diretorioRaiz, projetos):
        for rf in self.references:
            projeto = filtroProjeto(rf, projetos)
            if projeto == "":
                print("[ERRO][referenciar] => Projeto "+rf+" não encontrado")
                return

            # mudando para o diretorio onde ficara o projeto
            self.mudarDiretorio(diretorioRaiz+self.caminho)
            comando = "dotnet add "+self.projeto+" reference " + \
                diretorioRaiz+"\\"+projeto.caminho+"\\"+projeto.projeto
            comando = comando.replace(".cs", ".csproj")
            os.system(comando)

    def gerar(self, diretorioBase):
        print('Gerando projeto '+self.identificador)
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

        self.GerarTemplates(diretorioBase)
