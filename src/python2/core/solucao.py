import os
import sys

from core.diretorio import Diretorio


class Solucao():

    def __init__(self, nome, diretorio, usuarioGit, arquitetura):
        self.nome = nome
        self.diretorioProjetos = diretorio
        self.diretorioRaiz = diretorio + "\\" + nome
        self.diretorioSRC = diretorio + "\\" + nome+ "\\src"
        self.usuarioGit = usuarioGit
        self.arquitetura = arquitetura
        self.projetos = []

    def gerar(self):
        print('Gerar Solucao: '+self.nome)
        Diretorio.mudar(self.diretorioSRC)
        comando = 'dotnet new sln --name ' + self.nome
        os.system(comando)        
