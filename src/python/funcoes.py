import os
from leitor_json import retornaArquitetura

def filtroProjeto(nome, projetos):
    for projeto in projetos:
        if projeto.identificador == nome:
           return projeto
    pass