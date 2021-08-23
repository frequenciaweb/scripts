import os
import sys

class ConfiguracaoProjeto:
    def __init__(self,identificador, solucao,pasta, cli, packages = [] ):    
     self.identificador = identificador
     self.nome = solucao
     self.cli = cli.replace("%nameSolution%",solucao)+ " --output="+pasta
     self.dotnet =  cli.index("dotnet") >= 0 # identificar se o comando é dotnet ou npm
     self.projeto = self.nome+"."+identificador+".cs"
     self.caminho = pasta
     self.packages = packages

     if (cli == 'angular'):
         self.cli = "ng new "+identificador
         self.projeto = ""
         self.caminho = pasta+"\\"+self.nome
     if (cli == 'vue'):
         self.cli = "vue create "+identificador
         self.projeto = ""
         self.caminho = pasta+"\\"+self.nome

    def gerar(self):
        print('Gerando projeto '+self.identificador) 
            
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
      
        print('Instalando pacotes')             
        if (self.dotnet):
            for pk in self.packages:
                os.system("dotnet add package "+pk)

        if (self.dotnet == 'false'):
            for pk in self.packages:
                os.system("npm install -g "+pk)