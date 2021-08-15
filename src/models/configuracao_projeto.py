import os
import sys

class ConfiguracaoProjeto:
    def __init__(self,identificador, solucao,pasta, cli ):    
     self.identificador = identificador
     self.nome = solucao
     self.cli = "dotnet new "+cli+" --name="+self.nome+"."+identificador+" --output="+pasta+"\\"+self.nome+"."+identificador
     self.projeto = self.nome+"."+identificador+".cs"
     self.caminho = pasta+"\\"+self.nome+".Domain"

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
            os.chdir(self.diretorio)# mudando para o diretorio onde ficara o projeto
            os.system(self.cli) 
            os.system("ng build") 

        if (self.cli == 'vue'):
            os.chdir(self.diretorio)# mudando para o diretorio onde ficara o projeto            
            os.system("npm run build") 

        if (self.cli != 'vue' and self.cli != 'angular'):
            os.system(self.cli)