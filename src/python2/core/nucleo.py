import os
import sys
import subprocess as sp
import pandas as pd
import numpy as np

from core.diretorio import Diretorio
from core.projeto import Projeto


class Nucleo():

    def __init__(self):
        self.diretorioBot = os.getcwd()  # Diretorio onde está o bot
        self.solucao = {}

    def criarGlobalJson(self):
        print('Criar Global JSON')
        versionSDK = sp.run("dotnet --version", capture_output=True, text=True)
        SDK = versionSDK.stdout.replace("\n", "")
        SDK = SDK.replace("\r", "")
        print("Criando globalJSon versão "+SDK)

        # mantendo versão do sdk para todos os projetos
        self.executarComando("dotnet new globaljson --sdk-version " + SDK)

    def executarComando(self, comando):
        os.system(comando)

    def iniciarGit(self):
        print('Iniciar Git')
        self.executarComando("git init && dotnet new gitignore && echo # Projeto " +
                             self.solucao.nome+" >> README.md")  # inicializando o git

    def apagarDiretorio(self):
        Diretorio.mudar(self.solucao.diretorioProjetos)
        print('Apagar Diretório '+self.solucao.diretorioRaiz)
        comando = "rd "+self.solucao.nome+" /s /q"
        # Removendo o diretorio da solução caso ele já existe
        self.executarComando(comando)

    def retornaArquitetura(self, index):
        try:
            Diretorio.mudar(self.diretorioBot)
            arquivo = self.diretorioBot + "/src/python/config/arquitectures.json"
            if (os.path.exists(arquivo)):
                obj = pd.read_json(arquivo)
            return obj["arquitecutres"][index]

        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
            raise Exception("Erro ao ler arquivo de configuração")

    def carregarArquitetura(self):
        print('Carregar Arquitetura')
        # Carregando o json da arquitetura selecionada
        arquitetura = self.retornaArquitetura(
            int(self.solucao.arquitetura) - 1)
        print("Template: "+arquitetura['name'])
        projetos = []
        for projeto in arquitetura['projects']:
            folder = projeto['folder']
            folder = folder.replace("%nameSolution%", self.solucao.nome)
            projetos.append(Projeto(projeto['name'], self.solucao.nome, projeto['folder'], projeto['cli'],
                            projeto['packages'], projeto['references'], projeto['folders'], projeto['templates']))
        return projetos

    def referenciar(self, solucao, projeto):
        caminhoSolucao = solucao.diretorioSRC
        caminhoProjeto = projeto.caminho
        self.executarComando("dotnet sln "+caminhoSolucao+"\\" + solucao.nome+".sln add "+caminhoProjeto+"\\"+projeto['nome']+".csproj")

    def criarDiretoriosPadrao(self):
        print('Criar Diretórios Padrão')

        # criando o diretorio raiz onde ficara a pasta do projeto
        Diretorio.criar(self.solucao.diretorioRaiz)
        # mudando para o diretorio raiz onde ficara a pasta do projeto
        Diretorio.mudar(self.solucao.diretorioRaiz)
        Diretorio.criar(self.solucao.diretorioSRC)  # criando pasta de src
        # criando pasta de documentos
        Diretorio.criar(self.solucao.diretorioRaiz+"\docs")
        Diretorio.criarComArquivoExemplo(
            self.solucao.diretorioRaiz+"\docs\\diagramas", "Pasta de Diagramas do Sistema")  # criando pasta de diagramas
        Diretorio.criarComArquivoExemplo(
            self.solucao.diretorioRaiz+"\docs\\scripts",  "Pasta de Scripts do Sistema")  # criando pasta de scripts
        Diretorio.criarComArquivoExemplo(self.solucao.diretorioRaiz+"\docs\\casos de usos",
                                         "Pasta de casos de uso do Sistema")  # criando pasta de casos de usos
        Diretorio.criarComArquivoExemplo(self.solucao.diretorioRaiz+"\docs\\requisitos",
                                         "Pasta de Requisitos do Sistema")  # criando pasta de requisitos
        Diretorio.criarComArquivoExemplo(self.solucao.diretorioRaiz+"\docs\\arquitetura",
                                         "Pasta de Arquitetura do Sistema")  # criando pasta de arquitetura

    def build(self):
        print('Compilando')
        self.executarComando("dotnet build")

    def PrimeiroCommit(self):
        print('Primeiro Commit')
        self.executarComando(
            "git add * && git commit -m \"Primeiro Commit\" && git remote add origin https://github.com/%usuarioGit%/%namespace%.git && git push")

    def apagarArquivosDesnecessarios(self):
        print('Apagar Arquivos Desnecessarios')
        self.executarComando(
            "del Class1.cs /s && del UnitTest1.cs /s && del WeatherForecast.cs /s && del WeatherForecastController.cs /s")

    def gerarEstrutura(self):
        print('Gerar Estrutura')

        self.apagarDiretorio()
        self.criarDiretoriosPadrao()
        self.iniciarGit()
        self.criarGlobalJson()

        self.solucao.gerar()

        self.solucao.projetos = self.carregarArquitetura()
        self.gerarProjetos()

        Diretorio.mudar(self.solucao.diretorioSRC)

        self.referenciarProjetos()

        self.apagarArquivosDesnecessarios()
        self.build()
        self.PrimeiroCommit()

        self.executarComando("code .")

    def referenciarProjetos(self):
        Diretorio.mudar(self.solucao.diretorioSRC)
        for projeto in self.solucao.projetos:
            self.referenciar(self.solucao, projeto)

    def gerarProjetos(self):
        Diretorio.mudar(self.solucao.diretorioSRC)
        for projeto in self.solucao.projetos:
            Diretorio.mudar(self.solucao.diretorioSRC)
            projeto.gerar()

    def gerarSolucao(self, solucao):
        print('Gerar Solução')
        self.solucao = solucao
        self.gerarEstrutura()
