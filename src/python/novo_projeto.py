import os
import sys
import pandas as pd
import numpy as np
from models.projeto import Projeto
from models.configuracao_projeto import ConfiguracaoProjeto
from leitor_json import listarArquiteturas
from leitor_json import retornaArquitetura

def removendoArquivosDesnecessarios():
   executarComando('del Class1.cs /s')
   executarComando('del UnitTest1.cs /s')
   executarComando('del WeatherForecast.cs /s')
   executarComando('del WeatherForecastController.cs /s')

def limparTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def executarComando(comando):
    os.system(comando)

def adicionarProjetoNaSolucao(solucao,projeto):
    executarComando("dotnet sln "+solucao+".sln add "+projeto.caminho)    

def mudarDiretorio(nome):
    atual = os.getcwd()
    if (atual != nome):
       print('Mudando de '+atual+' para '+nome)
       os.chdir(nome) 

def gerarArquitetura(index, solucao, diretorioBase): 
   # Carregando o json da arquitetura selecionada
    arquitetura = retornaArquitetura(int(index)-1, diretorioBase)
    print("Template: "+arquitetura['name'])
    projetos = []
    for projeto in arquitetura['projects']:
        folder = projeto['folder']
        folder = folder.replace("%nameSolution%", solucao)        
        projetos.append(ConfiguracaoProjeto(projeto['name'],solucao,folder,projeto['cli'], projeto['packages'],projeto['references'], projeto['folders']))
        
    return projetos

def diretoriosPadroes(diretorio):
    os.makedirs(diretorio+"\docs")# criando pasta de documentos
    os.makedirs(diretorio+"\docs\\diagramas")# criando pasta de diagramas
    os.makedirs(diretorio+"\docs\\scripts")# criando pasta de scripts
    os.makedirs(diretorio+"\docs\\casos de usos")# criando pasta de scripts
    os.makedirs(diretorio+"\docs\\arquitetura")# criando pasta de scripts

def configurarProjeto(nome, diretorio, usuario, tipo, arquitetura, diretorioBase):

    diretorioRaiz = diretorio
    diretorioSrc = diretorio+ "/" + nome+"/src/"
    diretorioProjeto = diretorio+ "/" + nome+"/"
    
    mudarDiretorio(diretorioRaiz)# mudando para o diretorio raiz onde ficara a pasta do projeto
  
    executarComando("rd "+nome+" /s /q")# Removendo o diretorio da solu????o caso ele j?? existe    

    os.makedirs(diretorioSrc)# criando diretorio do projeto
    diretoriosPadroes(diretorioProjeto)

    mudarDiretorio(diretorioSrc)# mudando para o diretorio do projeto    

    # Preparando o projeto
    projeto = Projeto(nome,diretorioSrc,tipo,arquitetura,usuario)
    projeto.gerarSolucao()    
    
    mudarDiretorio(diretorioProjeto)# mudando para o diretorio da solu????o    
   
    executarComando("git init && dotnet new gitignore && echo # Projeto "+nome+" >> README.md")# inicializando o git    
    
    mudarDiretorio(diretorioSrc)# mudando para o diretorio do projeto    
    
    # Verificando qual arquitetura foi escolhida
    # Executando a configura????o
    projetos = gerarArquitetura(projeto.arquitetura,nome, diretorioBase)    
 
    for projeto in projetos:
        projeto.gerar()
        mudarDiretorio(diretorioSrc)# mudando para o diretorio do projeto    
        adicionarProjetoNaSolucao(nome, projeto)

    # print('Referenciando projetos')
    # for projeto in projetos:
    #     projeto.referenciar(diretorioSrc, projetos)

    # Deletando os arquivos desnecessarios     
    removendoArquivosDesnecessarios()
   
    # Compilando os projeto
    executarComando('dotnet build')
    
    mudarDiretorio(diretorioSrc)# mudando para o diretorio do projeto    
    # Executando primeiro commit
    print('Realizando primeiro commit')
    executarComando("git add * && git commit -m \"Primeiro commit\"")

    print('Abrindo VS Code')
    executarComando("code .")
            
def gerarNovoProjeto(diretorioBase, acao, debug = 'false'):
    
    limparTela()
   
    nome = ""
    diretorio = ""
    usuario = ""
    tipo = ""
    arquitetura = ""     
    confirma = ""     

    if (debug == 'true'):    
       nome = "TestandoBotPython"
       diretorio = "D:\Teste"
       usuario = ""
       tipo = "3"
       arquitetura = "1"        
       confirma = "1"        
    else:
        nome = input("Escolha o Nome para Solu????o: ")    
        diretorio = input("Escolha o diret??rio: ")     
        usuario = input("Informe Usu??rio do GitHub para Preparar o git (opcional): ")    
        tipo = input('''Escolha O Tipo de Projeto:
        ( 1 ) MVC
        ( 2 ) API
        ( 3 ) MVC + API
        ( 4 ) ANGULAR + API
        ( 5 ) VUEJS + API
        Escolha: ''')
        
        arquitetura = input(f'''Arquitetura
           {listarArquiteturas(diretorioBase)}
        ''') 
        
        if acao == '2':
           solucoes = input('Digte separado por virgula o nome da cada Dominio: ')

        confirma = input(f'''GERADOR DE PROJETOS
        Solution" , { nome },
        Path" , { diretorio },
        Git" , { usuario },
        Tipo" , { tipo },
        
        Confirma os dados?:
        ( 0 ) N??o
        ( 1 ) Sim
        Confirma????o: ''')      

    limparTela()
    print('Aguarde....')

    #Verificando resposta se deve contunar oprocesso    
    if confirma == "1" :     
       configurarProjeto(nome, diretorio, usuario, tipo, arquitetura, diretorioBase)
    