$(document).ready(function(){
  $("#Оформить").click(function(){
	   $(".print").printElement({pageTitle:'Отчет',overrideElementCSS:[
        "/media/style1.css",
        { href:'/media/style1.css'}]
            });
	});	
});