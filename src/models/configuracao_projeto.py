import os
import sys

class ConfiguracaoProjeto:
    def __init__(self,identificador, solucao,pasta, cli ):    
     self.identificador = identificador
     self.nome = solucao
     self.cli = "dotnet new "+cli+" --name="+self.nome+"."+identificador+" --output="+pasta+"\\"+self.nome+"."+identificador
     self.projeto = self.nome+"."+identificador+".cs"
     self.caminho = pasta+"\\"+self.nome+".Domain"

    def gerar(self):
        print('Gerando projeto '+self.identificador) 
        os.system(self.cli) 