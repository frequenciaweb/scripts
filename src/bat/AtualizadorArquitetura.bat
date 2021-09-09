@Echo off

echo 'Aguarde......'
set entidade=%1
set entidade=%entidade:"=%
set namespace=%2
set namespace=%namespace:~0,-5%
set namespace=%namespace:"=%
set nameContext=%namespace%Context

echo Gerando Arquivos para Entidade '%entidade%' Solution '%namespace%' DBContext '%nameContext%'

set diretorioSRC=%cd%

echo Criando Service Base
CALL :ServiceBase %namespace% %nameContext% > %diretorioSRC%\Domain\%namespace%.Domain.Services\Services\ServiceBase.cs
echo Criando Repositorie Base
CALL :RepositorieBase %namespace% %nameContext% > %diretorioSRC%\Infra\%namespace%.Infra.Data\Repositories\RepositorieBase.cs 
echo Criando Contrato de Repositorio Base
CALL :IRepositorieBase %namespace% %nameContext% > %diretorioSRC%\Domain\%namespace%.Domain\Contracts\Repositories\IRepositorieBase.cs
echo Criando Contrato de Servico Base
CALL :IServiceBase %namespace% %nameContext% > %diretorioSRC%\Domain\%namespace%.Domain\Contracts\Services\IServiceBase.cs
echo Criando Contrato de Repositorio 
CALL :contrato_repo %entidade% %namespace% %nameContext% > %diretorioSRC%\Domain\%namespace%.Domain\Contracts\Repositories\IRepositorie%entidade%.cs  
echo Implementando Contrato de Repositorio
CALL :implementacao_repo %entidade% %namespace% %nameContext% > %diretorioSRC%\Infra\%namespace%.Infra.Data\Repositories\Repositorie%entidade%.cs  
echo Criando Contrato de Servico
CALL :contrato_serv %entidade% %namespace% %nameContext% > %diretorioSRC%\Domain\%namespace%.Domain\Contracts\Services\IService%entidade%.cs  
echo Implementando Contrato de Servico
CALL :implementacao_serv %entidade% %namespace% %nameContext% > %diretorioSRC%\Domain\%namespace%.Domain.Services\Services\Service%entidade%.cs     

cd %diretorioSRC%\UI\%namespace%.UI.MVC
echo Gerando Views e controle temporario
dotnet aspnet-codegenerator --project %namespace%.UI.MVC.csproj  controller -name %entidade%Controller -f -udl -m %entidade% -dc %nameContext%
del %entidade%Controller.cs /s /q

cd %diretorioSRC%

echo Controle
CALL :controller %entidade% %namespace% %nameContext% > %diretorioSRC%\UI\%namespace%.UI.MVC\Controllers\%entidade%Controller.cs  

echo 'Processo Concluido!'

:formataVariavel


exit /b

:IServiceBase
echo using System.Collections.Generic;
echo.
echo namespace %1.Domain.Contracts.Services
echo {
echo     public interface IServiceBase^<TEntity^> where TEntity : class
echo     {
echo         TEntity Add(TEntity entity);
echo         TEntity Update(TEntity entity);
echo         void Delete(TEntity entity);
echo         List^<string^> GetAllAnnotations();
echo     }
echo }

exit /b

:IRepositorieBase

echo using System;
echo using System.Collections.Generic;
echo.
echo namespace %1.Domain.Contracts.Repositories
echo {
echo     public interface IRepositorieBase^<TEntity^> where TEntity : class
echo     {
echo         TEntity Add(TEntity entity);
echo         TEntity Update(TEntity entity);
echo         void Delete(TEntity entity);
echo         TEntity Get(Guid id);
echo         List^<TEntity^> Get();
echo     }
echo }

exit /b

:RepositorieBase

echo using %1.Domain.Contracts.Repositories;
echo using %1.Infra.Data.EF;
echo using System.Collections.Generic;
echo using System.Linq;
echo using System;
echo.
echo namespace %1.Infra.Data.Repositories
echo {
echo     public class RepositorieBase^<TEntity^> : IRepositorieBase^<TEntity^> where TEntity : class
echo     {
echo         private readonly %2 context;
echo.
echo         public RepositorieBase(%2 context)
echo         {
echo             this.context = context;
echo         }
echo.
echo         public virtual TEntity Update(TEntity entity)
echo         {
echo             context.Set^<TEntity^>().Update(entity);
echo             return entity;
echo         }
echo.
echo         public virtual void Delete(TEntity entity)
echo         {
echo             context.Set^<TEntity^>().Remove(entity);
echo         }
echo.
echo         public virtual TEntity Add(TEntity entity)
echo         {
echo             context.Set^<TEntity^>().Add(entity);            
echo             return entity;
echo         }
echo.
echo         public virtual TEntity Get(Guid id)
echo         {
echo             return context.Set^<TEntity^>().Find(id);
echo         }
echo.
echo         public virtual List^<TEntity^> Get()
echo         {
echo             return context.Set^<TEntity^>().ToList();
echo         }
echo     }
echo }

exit /b

:EntityBase

echo using System;
echo namespace %1.Domain.Entities
echo {
echo     public abstract class EntityBase
echo     {
echo        public Guid ID {get; set;}
echo     }
echo }

exit /b

:ServiceBase

echo using %1.Domain.Contracts.Repositories;
echo using %1.Domain.Contracts.Services;
echo using %1.Infra.Data.EF;
echo using System.Collections.Generic;
echo.
echo namespace %1.Domain.Services
echo {
echo     public class ServiceBase^<TEntity^> : IServiceBase^<TEntity^> where TEntity : class
echo     {
echo         private readonly IRepositorieBase^<TEntity^> repositorieBase;
echo         private readonly %2 context;
echo         private readonly List^<string^> Annotations;
echo.
echo         public ServiceBase(IRepositorieBase^<TEntity^> repositorieBase, %2 context)
echo         {
echo             this.context = context;
echo             this.repositorieBase = repositorieBase;
echo             Annotations = new List^<string^>();
echo         }
echo.
echo         public virtual TEntity Update(TEntity entity)
echo         {
echo             entity = repositorieBase.Update(entity);
echo             Commit();
echo             return entity;
echo         }
echo.
echo         public virtual void Delete(TEntity entity)
echo         {
echo             repositorieBase.Delete(entity);
echo             Commit();
echo         }
echo.
echo         public virtual TEntity Add(TEntity entity)
echo         {
echo             entity = repositorieBase.Add(entity);
echo             Commit();
echo             return entity;
echo         }
echo.
echo         protected void Commit()
echo         {
echo             context.SaveChanges();
echo         }
echo.
echo         protected void IncludeAnnotation(string message)
echo         {
echo             Annotations.Add(message);
echo         }
echo.
echo         public List^<string^> GetAllAnnotations()
echo         {
echo            return Annotations;
echo         }
echo.
echo     }
echo }

exit /b

:entidade

echo using System;
echo using System.Collections.Generic;
echo.
echo namespace %2.Domain.Entities
echo {
echo    public class %1 : EntityBase {
echo. 
echo      public Guid ID {get; set;}
echo. 
echo    }
echo. 
echo }

exit /b

:controller

echo using %2.Domain.Contracts.Repositories;
echo using %2.Domain.Contracts.Services;
echo using %2.Domain.Entities;
echo using Microsoft.AspNetCore.Http;
echo using Microsoft.AspNetCore.Mvc;
echo using Microsoft.EntityFrameworkCore;
echo using System;
echo using System.Collections.Generic;
echo. 
echo namespace %2.UI.MVC.Controllers
echo {
echo     public class %1Controller : Controller
echo     {
echo         private IService%1 Service%1 { get; set; }
echo         private IRepositorie%1 Repositorie%1 { get; set; }
echo. 
echo         public %1Controller(IService%1 service%1, IRepositorie%1 repositorie%1)
echo         {
echo             Service%1 = service%1;
echo             Repositorie%1 = repositorie%1;
echo         }
echo. 
echo         // GET: %1s
echo         public IActionResult Index()
echo         {
echo             return View(Repositorie%1.Get());
echo         }
echo. 
echo         [HttpPost]
echo         public IActionResult Index(IFormCollection form)
echo         {
echo             if (string.IsNullOrEmpty(form["tipoPesquisa[]"]) ^|^| string.IsNullOrEmpty(form["valor[]"]))
echo             {
echo                 ViewBag.Erro = "Selecione os tipos de pesquisa e informe os valores";
echo                 return View(new List^<%1^>());
echo             }
echo.            
echo             return View(Repositorie%1.Get());
echo         }
echo. 
echo         // GET: %1s/Details/5
echo         public IActionResult Details(Guid? id)
echo         {
echo             if (id == null)
echo             {
echo                 return NotFound();
echo             }
echo. 
echo             %1 %1 = Repositorie%1.Get((Guid)id);
echo             if (%1 == null)
echo             {
echo                 return NotFound();
echo             }
echo. 
echo             return View(%1);
echo         }
echo.
echo         // GET: %1s/Create
echo         public IActionResult Create()
echo         {
echo             return View();
echo         }
echo. 
echo         // POST: %1s/Create
echo         // To protect from overposting attacks, enable the specific properties you want to bind to.
echo         // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
echo         [HttpPost]
echo         [ValidateAntiForgeryToken]
echo         public IActionResult Create(%1 %1)
echo         {
echo             if (ModelState.IsValid)
echo             {
echo                 Service%1.Add(%1);
echo                 return RedirectToAction(nameof(Index));
echo             }
echo             return View(%1);
echo         }
echo. 
echo         // GET: %1s/Edit/5
echo         public IActionResult Edit(Guid? id)
echo         {
echo             if (id == null)
echo             {
echo                 return NotFound();
echo             }
echo. 
echo             %1 %1 = Repositorie%1.Get((Guid)id);
echo. 
echo             if (%1 == null)
echo             {
echo                 return NotFound();
echo             }
echo             return View(%1);
echo         }
echo. 
echo         // POST: %1s/Edit/5
echo         // To protect from overposting attacks, enable the specific properties you want to bind to.
echo         // For more details, see http://go.microsoft.com/fwlink/?LinkId=317598.
echo         [HttpPost]
echo         [ValidateAntiForgeryToken]
echo         public IActionResult Edit(Guid id, %1 %1)
echo         {
echo             if (id != %1.ID)
echo             {
echo                 return NotFound();
echo             }
echo. 
echo             if (ModelState.IsValid)
echo             {
echo                 try
echo                 {
echo                     Service%1.Update(%1);
echo                 }
echo                 catch (DbUpdateConcurrencyException)
echo                 {
echo                     if (!%1Exists(%1.ID))
echo                     {
echo                         return NotFound();
echo                     }
echo                     else
echo                     {
echo                         throw;
echo                     }
echo                 }
echo                 return RedirectToAction(nameof(Index));
echo             }
echo             return View(%1);
echo         }
echo. 
echo         // GET: %1s/Delete/5
echo         public IActionResult Delete(Guid? id)
echo         {
echo             if (id == null)
echo             {
echo                 return NotFound();
echo             }
echo. 
echo             %1 %1 = Repositorie%1.Get((Guid)id);
echo             if (%1 == null)
echo             {
echo                 return NotFound();
echo             }
echo. 
echo             return View(%1);
echo         }
echo. 
echo         // POST: %1s/Delete/5
echo         [HttpPost, ActionName("Delete")]
echo         [ValidateAntiForgeryToken]
echo         public IActionResult DeleteConfirmed(Guid id)
echo         {
echo             var %1 = Repositorie%1.Get(id);
echo             if (%1 == null)
echo             {
echo                 return NotFound();
echo             }
echo             Service%1.Delete(%1);
echo             return RedirectToAction(nameof(Index));
echo         }
echo. 
echo         private bool %1Exists(Guid id)
echo         {
echo             return Repositorie%1.Get(id) != null;
echo         }
echo     }
echo }



EXIT /B

:implementacao_serv

echo using %2.Domain.Contracts.Repositories;
echo using %2.Domain.Contracts.Services;
echo using %2.Domain.Entities;
echo using %2.Infra.Data.EF;
echo.
echo namespace %2.Domain.Services.Services
echo {
echo.
echo     public class Service%1 : ServiceBase^<%1^>, IService%1
echo     {
echo         private readonly IRepositorie%1 repositorie%1;
echo.
echo         public Service%1(IRepositorie%1 repo, %3 context) : base(repo, context)
echo         {
echo             repositorie%1 = repo;
echo         }
echo     }
echo }

EXIT /B

:contrato_serv

echo using %2.Domain.Contracts.Services;
echo using %2.Domain.Entities;
echo.
echo namespace %2.Domain.Contracts.Services 
echo {
echo     public interface IService%1 : IServiceBase^<%1^>
echo     {
echo.
echo     }
echo }

EXIT /B

:implementacao_repo

echo using %2.Domain.Contracts.Repositories;
echo using %2.Domain.Entities;
echo using %2.Infra.Data.EF;
echo.
echo namespace %2.Infra.Data.Repositories
echo {
echo     public class Repositorie%1 : RepositorieBase^<%1^>, IRepositorie%1
echo     {
echo         private %3 Context { get; set; }
echo.
echo         public Repositorie%1(%3 context) : base(context)
echo         {
echo             Context = context;
echo         }
echo     }
echo }

EXIT /B

:contrato_repo

echo using %2.Domain.Entities;
echo.
echo namespace %2.Domain.Contracts.Repositories
echo {
echo     public interface IRepositorie%1 : IRepositorieBase^<%1^>
echo     {
echo     }
echo }

EXIT /B

:dbcontext

echo using %1.Domain.Entities;
echo using Microsoft.EntityFrameworkCore;
echo. 
echo namespace %1.Infra.Data.EF
echo {
echo     public class %2 : DbContext
echo     {  
echo         public %2()
echo         {
echo. 
echo         }
echo. 		
echo         public %2(DbContextOptions options) : base(options)
echo         {
echo.
echo         }
echo. 
echo         protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
echo         {
echo             string connectionString = "server=localhost;uid=root;pwd=Ab134679;database=%1";
echo             optionsBuilder.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString));
echo         }
echo. 
echo         protected override void OnModelCreating(ModelBuilder modelBuilder)
echo         {
echo.            
echo         }
echo     }
echo }

exit /b

pause



