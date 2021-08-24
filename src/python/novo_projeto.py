import os
import sys
import pandas as pd
import numpy as np
from models.projeto import Projeto
from models.configuracao_projeto import ConfiguracaoProjeto
from leitor_json import listarArquiteturas
from leitor_json import retornaArquitetura

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
    print("Arquitetura: "+arquitetura['name'])
    projetos = []
    for projeto in arquitetura['projects']:
        folder = projeto['folder']
        folder = folder.replace("%nameSolution%", solucao)        
        projetos.append(ConfiguracaoProjeto(projeto['name'],solucao,folder,projeto['cli'], projeto['packages'],projeto['references']))
        
    return projetos

def configurarProjeto(nome, diretorio, usuario, tipo, arquitetura, diretorioBase):

    diretorioRaiz = diretorio
    diretorioSrc = diretorio+ "/" + nome+"/src/"
    diretorioProjeto = diretorio+ "/" + nome+"/"
    
    mudarDiretorio(diretorioRaiz)# mudando para o diretorio raiz onde ficara a pasta do projeto
  
    executarComando("rd "+nome+" /s /q")# Removendo o diretorio da solução caso ele já existe    

    os.makedirs(diretorioSrc)# criando diretorio do projeto

    mudarDiretorio(diretorioSrc)# mudando para o diretorio do projeto    

    # Preparando o projeto
    projeto = Projeto(nome,diretorioSrc,tipo,arquitetura,usuario)
    projeto.gerarSolucao()    
    
    mudarDiretorio(diretorioProjeto)# mudando para o diretorio da solução    

    executarComando("git init && dotnet new gitignore && echo # Projeto "+nome+" >> README.md")# inicializando o git    
    
    mudarDiretorio(diretorioSrc)# mudando para o diretorio do projeto    
    
    # Verificando qual arquitetura foi escolhida
    # Executando a configuração
    projetos = gerarArquitetura(projeto.arquitetura,nome, diretorioBase)    

    if (tipo == "1"):
       projetos.append(ConfiguracaoProjeto("UI.MVC",nome,"UI/%nameSolution%.UI.MVC","dotnet new mvc --name=%nameSolution%.UI.MVC"))

    if (tipo == "2"):
       projetos.append(ConfiguracaoProjeto("Api",nome,"API/%nameSolution%.API","dotnet new webapi --name=%nameSolution%.API"))

    if (tipo == "3"):
       projetos.append(ConfiguracaoProjeto("Api",nome,"API/%nameSolution%.API","dotnet new webapi --name=%nameSolution%.API"))
       projetos.append(ConfiguracaoProjeto("UI.MVC",nome,"UI/%nameSolution%.UI.MVC","dotnet new mvc --name=%nameSolution%.UI.MVC"))
    
    if (tipo == "4"):
       projetos.append(ConfiguracaoProjeto("Api",nome,"API/%nameSolution%.API","dotnet new webapi --name=%nameSolution%.API"))
       projetos.append(ConfiguracaoProjeto("UI.Site",nome,"UI","angular"))
       
    if (tipo == "5"):
       projetos.append(ConfiguracaoProjeto("Api",nome,"API/%nameSolution%.API","dotnet new webapi --name=%nameSolution%.API"))
       projetos.append(ConfiguracaoProjeto("UI.Site",nome,"UI","vue"))
 
    for projeto in projetos:
        projeto.gerar()
        mudarDiretorio(diretorioSrc)# mudando para o diretorio do projeto    
        adicionarProjetoNaSolucao(nome, projeto)

    # print('Referenciando projetos')
    # for projeto in projetos:
    #     projeto.referenciar(diretorioSrc, projetos)

    # Deletando os arquivos desnecessarios 
    
    executarComando('del Class1.cs /s')
    executarComando('del UnitTest1.cs /s')
    executarComando('del WeatherForecast.cs /s')
    executarComando('del WeatherForecastController.cs /s')
   
    # Compilando os projeto
    executarComando('dotnet build')
    
    mudarDiretorio(diretorioSrc)# mudando para o diretorio do projeto    
    # Executando primeiro commit
    print('Realizando primeiro commit')
    executarComando("git add * && git commit -m \"Primeiro commit\"")
    

            
def gerarNovoProjeto(diretorioBase, acao, debug = 'false'):
    
    executarComando('cls' if os.name == 'nt' else 'clear')
   
    nome = ""
    diretorio = ""
    usuario = ""
    tipo = ""
    arquitetura = ""     
    confirma = ""     

    if (debug == 'true'):    
       nome = "TestandoBot"
       diretorio = "D:\Projetos"
       usuario = ""
       tipo = "3"
       arquitetura = "1"        
       confirma = "1"        
    else:
        nome = input("Escolha o Nome para Solução: ")    
        diretorio = input("Escolha o diretório: ")     
        usuario = input("Informe Usuário do GitHub para Preparar o git (opcional): ")    
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
        ( 0 ) Não
        ( 1 ) Sim
        Confirmação: ''')      

    executarComando('cls' if os.name == 'nt' else 'clear')
    print('Aguarde....')

    #Verificando resposta se deve contunar oprocesso    
    if confirma == "1" :     
       configurarProjeto(nome, diretorio, usuario, tipo, arquitetura, diretorioBase)
    