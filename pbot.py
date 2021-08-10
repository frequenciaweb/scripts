import os
import sys

os.system('cls' if os.name == 'nt' else 'clear')

version = 1.2

print("Bem vindo ao Gerador de Projetos 1.2 \n"
"Requisitos Basicos \n"
"- NetCore SDK \n"
"- NPM \n"
"- Pacote Angular \n"
"- Pacote VueJS \n"
"- Git")

print("Escolha o Nome para Solução:")
namespace = input()

os.system('cls' if os.name == 'nt' else 'clear')

print("GERADOR DE PROJETOS", version ,
    "\n Escolha o Diretório para o Projeto:")
diretorio = input()

os.system('cls' if os.name == 'nt' else 'clear')

print("GERADOR DE PROJETOS", version ,
    "\n Informe Usuário do GitHub para Preparar o git:")
usuarioGit = input()

os.system('cls' if os.name == 'nt' else 'clear')

print("GERADOR DE PROJETOS", version ,
    "\n Escolha O Tipo de Projeto \n"
    "( 1 ) MVC \n"
    "( 2 ) API \n"
    "( 3 ) MVC + API \n"
    "( 4 ) ANGULAR + API \n"
    "( 5 ) VUEJS + API \n"
    )
projeto = input()

os.system('cls' if os.name == 'nt' else 'clear')

print("GERADOR DE PROJETOS", version ,
    "\n Qual IDE Vai Usar?: \n"
    "( 0 ) Nenhuma"
    "( 1 ) Nenhuma"
    "( 2 ) Nenhuma"
    )
ide = input()

os.system('cls' if os.name == 'nt' else 'clear')

print("GERADOR DE PROJETOS", version ,
    "\n Solution" , namespace,
    "\n Path" , diretorio,
    "\n Git" , usuarioGit,
    "\n ",
    "\n Confirma os dados?: \n"
    "( 0 ) Não"
    "( 1 ) Sim"    
    )
    
confirma = input()    

def end():
    print('Processo Finalizou')

def iniciar():  
  os.system('cls' if os.name == 'nt' else 'clear')
  print('Aguarde...!')  

  os.chdir(diretorio)

diretorioRaiz = os.getcwd()

if confirma == "1" :     
   iniciar()
else:   
  end()


 



