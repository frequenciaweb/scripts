import os
import sys
from src.models.projeto import Projeto
from src.models.configuracao_projeto import ConfiguracaoProjeto

def adicionarProjetoNaSolucao(solucao,projeto):
    comando = "dotnet sln "+solucao+".sln add "+projeto.caminho
    os.system(comando)

def mudarDiretorio(nome):
    atual = os.getcwd()
    if (atual != nome):
       os.chdir(nome) 

def gerarArquiteturaCleanArquitecture(nome):
    print('falta implementar')

def gerarArquiteturaDDD(nome): 
     os.mkdir('UI')
     os.mkdir('Domain')
     os.mkdir('Infra')
     os.mkdir('Test')
     return configura_camadas_arquitetura(nome)

def configura_camadas_arquitetura(nome):
    projetos = []
    projetos.append(ConfiguracaoProjeto("Domain",nome,"Domain","classlib"))     
    projetos.append(ConfiguracaoProjeto("Domain.Service",nome,"Domain","classlib")) 
    projetos.append(ConfiguracaoProjeto("Infra.Data",nome,"Infra","classlib"))
    projetos.append(ConfiguracaoProjeto("Infra.CorssCutting",nome,"Infra","classlib"))
    projetos.append(ConfiguracaoProjeto("Test",nome,"Test","msTest"))    
    return projetos

def configurarProjeto(nome, diretorio, usuario, tipo, arquitetura):

    mudarDiretorio(diretorio)# mudando para o diretorio raiz onde ficara o projeto
    
    comando = "rd "+nome+" /s /q"
    os.system(comando)# Removendo o diretorio da solução caso ele já existe

    # Preparando o projeto
    projeto = Projeto(nome,diretorio,tipo,arquitetura,usuario)
    projeto.gerarSolucao()    
    
    mudarDiretorio(nome)#mudando para o diretorio do projeto

    # Verificando qual arquitetura foi escolhida
    # Executando a configuração
    projetos = []    
    if projeto.arquitetura == "1":
       projetos = gerarArquiteturaDDD(nome)

    if projeto.arquitetura == "2":
       projetos = gerarArquiteturaCleanArquitecture(nome)       

    if (tipo == "1"):
       projetos.append(ConfiguracaoProjeto("UI.MVC",nome,"UI","mvc"))

    if (tipo == "2"):
       projetos.append(ConfiguracaoProjeto("Api",nome,"Api","webapi"))

    if (tipo == "3"):
       projetos.append(ConfiguracaoProjeto("Api",nome,"Api","webapi"))
       projetos.append(ConfiguracaoProjeto("UI.MVC",nome,"UI","mvc"))
    
    if (tipo == "4"):
       projetos.append(ConfiguracaoProjeto("Api",nome,"Api","webapi"))
       projetos.append(ConfiguracaoProjeto("UI.Site",nome,"UI","angular"))
       
    if (tipo == "5"):
       projetos.append(ConfiguracaoProjeto("Api",nome,"Api","webapi"))
       projetos.append(ConfiguracaoProjeto("UI.Site",nome,"UI","vue"))
 
    for projeto in projetos:
        projeto.gerar()
        adicionarProjetoNaSolucao(nome, projeto)
   

    mudarDiretorio(nome)#mudando para o diretorio do projeto
    #Deletando os arquivos desnecessarios 
    os.system('del Class1.cs /s')
    os.system('del UnitTest1.cs /s')
    os.system('del WeatherForecast.cs /s')
    os.system('del WeatherForecastController.cs /s')
   
    #Compilando os projeto
    os.system('dotnet build')
    
def gerarNovoProjeto(debug):
    os.system('cls' if os.name == 'nt' else 'clear')
   
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

        arquitetura = input('''Arquitetura
        ( 1 ) Driven Domain Design 
        ( 2 ) Clean Arquitecture
        ''')  

        confirma = input(f'''GERADOR DE PROJETOS
        Solution" , { nome },
        Path" , { diretorio },
        Git" , { usuario },
        Tipo" , { tipo },
        
        Confirma os dados?:
        ( 0 ) Não
        ( 1 ) Sim
        Confirmação: ''')      

    os.system('cls' if os.name == 'nt' else 'clear')
    print('Aguarde....')

    #Verificando resposta se deve contunar oprocesso    
    if confirma == "1" :     
       configurarProjeto(nome, diretorio, usuario, tipo, arquitetura)
    