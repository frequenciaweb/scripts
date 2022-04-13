import os
import sys

from funcoes import filtroProjeto

class  ConfiguracaoProjeto:
    def __init__(self,identificador, solucao,pasta, cli, packages = [], references = [], folders = [] ):    
     self.identificador = identificador
     self.nome = solucao
     pasta = pasta.replace("%nameSolution%",solucao)
     self.cli = cli.replace("%nameSolution%",solucao)+ " --output="+pasta     
     self.dotnet =  cli.index("dotnet") >= 0 # identificar se o comando é dotnet ou npm
     self.projeto = self.nome+"."+identificador+".cs"
     self.caminho = pasta
     self.references = references
     self.packages = packages
     self.folders = folders

     if (cli == 'angular'):
         self.cli = "ng new "+identificador
         self.projeto = ""
         self.caminho = pasta+"\\"+self.nome
     if (cli == 'vue'):
         self.cli = "vue create "+identificador
         self.projeto = ""
         self.caminho = pasta+"\\"+self.nome


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
            projeto = filtroProjeto(rf,projetos)     
            os.chdir(self.caminho)# mudando para o diretorio onde ficara o projeto       
            comando = "dotnet add "+self.projeto+" reference "+diretorioRaiz+"\\"+projeto.caminho+"\\"+projeto.projeto
            os.system(comando)            

    def gerar(self):
        print('Gerando projeto '+self.identificador) 
        os.makedirs(self.caminho)
        if (self.cli == 'angular'):
            os.chdir(self.caminho)# mudando para o diretorio onde ficara o projeto
            os.system(self.cli) 
            os.system("ng build") 

        if (self.cli == 'vue'):
            os.chdir(self.caminho)# mudando para o diretorio onde ficara o projeto
            os.system("npm run build") 

        if (self.cli != 'vue' and self.cli != 'angular'):
            os.system(self.cli)
            os.chdir(self.caminho)# mudando para o diretorio onde ficara o projeto
      
        if (self.dotnet):
            self.dotNet()

        if (self.dotnet == 'false'):
            for pk in self.packages:
                os.system("npm install -g "+pk)              

   