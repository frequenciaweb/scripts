import os
import pandas as pd
import numpy as np
import sys

def retornaArquitetura(index, diretorioBase):
    try:      
        local = diretorioBase
        arquivo = local + "/src/python/config/arquitectures.json"
        if (os.path.exists(arquivo)):
           obj = pd.read_json(arquivo)        

        arquivo = local + "/python/config/arquitectures.json"
        if (os.path.exists(arquivo)):
           obj = pd.read_json(arquivo)                   
           
        return obj["arquitecutres"][index]
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")        
        raise Exception("Erro ao ler arquivo de configuração")

def listarArquiteturas(diretorioBase):
    try:     
        local = os.getcwd();               
        obj = pd.read_json("src/python/config/arquitectures.json")
        texto = ""
        contador = 1             
        for a in obj["arquitecutres"]:            
            texto +=f'''( {contador} ) - {a['name']}'''          
            texto += "\n"            
            contador = contador + 1                
            
        return texto+":"       
    except Exception as e:
        print("Oops!", e.__class__, "occurred.")        
        raise Exception("Erro ao ler arquivo de configuração")