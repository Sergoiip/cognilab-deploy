// Cogsmos · Puente de mando — marca la vista actual en el selector común
(function(){
  const p=location.pathname.replace(/\/$/,"")||"/";
  const v=p==="/"||p==="/mapa"?"mapa":p.slice(1);
  document.querySelectorAll(".vistas a").forEach(a=>{if(a.dataset.v===v)a.setAttribute("aria-current","page")});
})();
