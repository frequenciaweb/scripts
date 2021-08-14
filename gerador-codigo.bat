@Echo off

set entidades=Perfil
set namespace=LojaVirtual

md Codigos\Contratos\Repositorios
md Codigos\Contratos\Servicos
md Codigos\Implementacoes\Repositorios
md Codigos\Implementacoes\Servicos
md Codigos\Controllers

FOR %%E in (%entidades%) do (
   CALL :contrato_repo %%E %namespace% > Codigos\Contratos\Repositorios\IRepositorie%%E.cs  
   CALL :implementacao_repo %%E %namespace% > Codigos\Implementacoes\Repositorios\Repositorie%%E.cs  
   CALL :contrato_serv %%E %namespace% > Codigos\Contratos\Servicos\IService%%E.cs  
   CALL :implementacao_serv %%E %namespace% > Codigos\Implementacoes\Servicos\Service%%E.cs  
   CALL :controller %%E %namespace% > Codigos\Controllers\%%EController.cs  
)

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
echo             return View(Repositorie%1.Obter());
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
echo             return View(Repositorie%1.Obter());
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
echo             %1 %1 = Repositorie%1.Obter((Guid)id);
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
echo                 Service%1.Incluir(%1);
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
echo             %1 %1 = Repositorie%1.Obter((Guid)id);
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
echo                     Service%1.Alterar(%1);
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
echo             %1 %1 = Repositorie%1.Obter((Guid)id);
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
echo             var %1 = Repositorie%1.Obter(id);
echo             if (%1 == null)
echo             {
echo                 return NotFound();
echo             }
echo             Service%1.Excluir(%1);
echo             return RedirectToAction(nameof(Index));
echo         }
echo. 
echo         private bool %1Exists(Guid id)
echo         {
echo             return Repositorie%1.Obter(id) != null;
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
echo         public Service%1(IRepositorie%1 repo, LojaVirtualContext context) : base(repo, context)
echo         {
echo.
echo         }
echo     }
echo }

EXIT /B

:contrato_serv

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
echo         private LojaVirtualContext Context { get; set; }
echo.
echo         public Repositorie%1(LojaVirtualContext context) : base(context)
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