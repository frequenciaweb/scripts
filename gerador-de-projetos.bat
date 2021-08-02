@echo off
cls

ECHO GERADOR DE PROJETOS

ECHO Escolha o nome para solucao
set /p namespace="Solution: "

ECHO Escolha o diretorio para o projeto
set /p diretorio="Diretorio: "

ECHO Informe usuario do github para preparar o git
set /p usuarioGit="Usuario git: "

ECHO Escolha O Tipo de Projeto
ECHO   ( 0 )   MVC

ECHO   ( 1 )   API

ECHO   ( 2 )   MVC + API

ECHO   ( 4 )   ANGULAR + API

ECHO   ( 5 )   VUEJS + API

set /p projeto="Projeto: "

ECHO Qual IDE vai usar?

ECHO   ( 0 )   Nenhuma

ECHO   ( 1 )   Visual Studio

ECHO   ( 2 )   Visual Studio Code


set /p ide="IDE: "

ECHO Aguarde alguns minutos........

cd\

cd %diretorio%
rd %namespace% /s /q

ECHO Criando a solucao %namespace%
dotnet new sln -o %namespace%
ECHO Aguarde........

cd %namespace%

set diretorioRaiz=%cd%

md Domain
md Infra
md Test

if %projeto%=='0'(set criarProjetoMVC=y)
if %projeto%=='1'(set criarProjetoApi=y)
if %projeto%=='2'(set criarProjetoApi=y&&set criarProjetoMVC=y)
if %projeto%=='4'(set criarProjetoApi=y&&set criarProjetoAngular=y)
if %projeto%=='5'(set criarProjetoApi=y&&set criarProjetoVUE=y)


echo '%projeto% Api (%criarProjetoApi%) MVC (%criarProjetoMVC%) Angular (%criarProjetoAngular%) Vue (%criarProjetoVUE%)'

pause

set caminhoProjetoDomain=Domain\%namespace%.Domain
set caminhoProjetoDomainService=Domain\%namespace%.Domain.Services
set caminhoProjetoInfraData=Infra\%namespace%.Infra.Data
set caminhoProjetoInfraCrossCutting=Infra\%namespace%.Infra.CrossCutting
set caminhoProjetoTest=Test\%namespace%.Test
set caminhoProjetoUIMVC=UI\%namespace%.UI.MVC
set caminhoProjetoAPI=Api\%namespace%.Api

set nomeProjetoDomain=%namespace%.Domain
set nomeProjetoDomainServcies=%namespace%.Domain.Services
set nomeProjetoInfraData=%namespace%.Infra.Data
set nomeProjetoInfraCrossCutting=%namespace%.Infra.CrossCutting
set nomeProjetoTest=%namespace%.Test
set nomeProjetoUIMVC=%namespace%.UI.MVC
set nomeProjetoAPI=%namespace%.Api

dotnet new classlib --name=%nomeProjetoDomain% --output=%caminhoProjetoDomain%
dotnet new classlib --name=%nomeProjetoDomainServcies% --output=%caminhoProjetoDomainService%
dotnet new classlib --name=%nomeProjetoInfraData% --output=%caminhoProjetoInfraData%
dotnet new classlib --name=%nomeProjetoInfraCrossCutting% --output=%caminhoProjetoInfraCrossCutting%
dotnet new msTest --name=%nomeProjetoTest% --output=%caminhoProjetoTest%

dotnet sln %namespace%.sln add %caminhoProjetoDomain%\%nomeProjetoDomain%.csproj
dotnet sln %namespace%.sln add %caminhoProjetoDomainService%\%nomeProjetoDomainServcies%.csproj
dotnet sln %namespace%.sln add %caminhoProjetoInfraData%\%nomeProjetoInfraData%.csproj
dotnet sln %namespace%.sln add %caminhoProjetoInfraCrossCutting%\%nomeProjetoInfraCrossCutting%.csproj
dotnet sln %namespace%.sln add %caminhoProjetoTest%\%nomeProjetoTest%.csproj

if %criarProjetoApi%==y (GOTO configura_api) else (GOTO configura_mvc) 

:configura_api

ECHO 'CRIANDO API'
md Api

dotnet new webapi --name=%nomeProjetoAPI% --output=%caminhoProjetoAPI%
dotnet sln %namespace%.sln add %caminhoProjetoAPI%\%nomeProjetoAPI%.csproj

cd %caminhoProjetoAPI%

dotnet add package Newtonsoft.Json
dotnet add package Microsoft.EntityFrameworkCore
dotnet add package Microsoft.EntityFrameworkCore.tools
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Pomelo.EntityFrameworkCore.MySql

dotnet add %nomeProjetoAPI%.csproj reference %diretorioRaiz%\%caminhoProjetoDomain%\%nomeProjetoDomain%.csproj
dotnet add %nomeProjetoAPI%.csproj reference %diretorioRaiz%\%caminhoProjetoDomainService%\%nomeProjetoDomainServcies%.csproj
dotnet add %nomeProjetoAPI%.csproj reference %diretorioRaiz%\%caminhoProjetoInfraData%\%nomeProjetoInfraData%.csproj
dotnet add %nomeProjetoAPI%.csproj reference %diretorioRaiz%\%caminhoProjetoInfraCrossCutting%\%nomeProjetoInfraCrossCutting%.csproj

cd %diretorioRaiz%

if %criarProjetoAngular%==y (GOTO configura_angular)  
if %criarProjetoVUE%==y (GOTO configura_vue)  
if %criarProjetoMVC%==y (GOTO configura_mvc)

GOTO finaliza

goto:eof


:configura_mvc
ECHO 'CRIANDO MVC'
md UI

dotnet new mvc --name=%nomeProjetoUIMVC% --output=%caminhoProjetoUIMVC%
dotnet sln %namespace%.sln add %caminhoProjetoUIMVC%\%nomeProjetoUIMVC%.csproj

cd %caminhoProjetoUIMVC%
dotnet add package Newtonsoft.Json
dotnet add package Microsoft.EntityFrameworkCore
dotnet add package Microsoft.EntityFrameworkCore.tools
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.AspNetCore.Mvc.Razor.RuntimeCompilation

dotnet add %nomeProjetoUIMVC%.csproj reference %diretorioRaiz%\%caminhoProjetoDomain%\%nomeProjetoDomain%.csproj
dotnet add %nomeProjetoUIMVC%.csproj reference %diretorioRaiz%\%caminhoProjetoDomainService%\%nomeProjetoDomainServcies%.csproj
dotnet add %nomeProjetoUIMVC%.csproj reference %diretorioRaiz%\%caminhoProjetoInfraData%\%nomeProjetoInfraData%.csproj
dotnet add %nomeProjetoUIMVC%.csproj reference %diretorioRaiz%\%caminhoProjetoInfraCrossCutting%\%nomeProjetoInfraCrossCutting%.csproj

cd %diretorioRaiz%
GOTO finaliza
goto:eof


:configura_angular
ECHO 'CRIANDO angular'
md UI
cd UI

ng new %namespace% 
ng build 

cd %diretorioRaiz%
GOTO finaliza
goto:eof

:configura_vue
ECHO 'CRIANDO vue'
md UI
cd UI
vue create %namespace% 
cd %diretorioRaiz%
GOTO finaliza

goto:eof

:finaliza
cd %diretorioRaiz%

cd %caminhoProjetoInfraData%
dotnet add package Microsoft.EntityFrameworkCore
dotnet add package Microsoft.EntityFrameworkCore.tools
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Pomelo.EntityFrameworkCore.MySql

cd %diretorioRaiz%


dotnet add %caminhoProjetoInfraData%\%nomeProjetoInfraData%.csproj reference %caminhoProjetoDomain%\%nomeProjetoDomain%.csproj

dotnet add %caminhoProjetoDomainService%\%nomeProjetoDomainServcies%.csproj reference %caminhoProjetoInfraData%\%nomeProjetoInfraData%.csproj
dotnet add %caminhoProjetoDomainService%\%nomeProjetoDomainServcies%.csproj reference %caminhoProjetoDomain%\%nomeProjetoDomain%.csproj
dotnet add %caminhoProjetoDomainService%\%nomeProjetoDomainServcies%.csproj reference %caminhoProjetoInfraCrossCutting%\%nomeProjetoInfraCrossCutting%.csproj

dotnet add %caminhoProjetoTest%\%nomeProjetoTest%.csproj reference %caminhoProjetoDomain%\%nomeProjetoDomain%.csproj
dotnet add %caminhoProjetoTest%\%nomeProjetoTest%.csproj reference %caminhoProjetoDomainService%\%nomeProjetoDomainServcies%.csproj
dotnet add %caminhoProjetoTest%\%nomeProjetoTest%.csproj reference %caminhoProjetoInfraData%\%nomeProjetoInfraData%.csproj
dotnet add %caminhoProjetoTest%\%nomeProjetoTest%.csproj reference %caminhoProjetoInfraCrossCutting%\%nomeProjetoInfraCrossCutting%.csproj

del Class1.cs /s
del UnitTest1.cs /s

git init
dotnet new gitignore

dotnet build

if %usuarioGit%=="" (GOTO abrir_ide) else (GOTO realizar_push)

goto:eof


:realizar_push

echo 'Enviar codigo para GIT'

git add *
git commit -m "Primeiro Commit"
git remote add origin https://github.com/%usuarioGit%/%namespace%.git
git push

GOTO abrir_ide

goto:eof

:abrir_ide
echo 'Abrir IDE'
if %ide%==1 (code .)
if %ide%==2 (%namespace%.sln)
goto:eof