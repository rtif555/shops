function clearChair(){
    $(".chr").hide()
    $("#id_quantity_of_legs").val("---------")
    $("#id_quantity_of_legs").hide()
    $("#id_height_spin").val("---------")
    $("#id_height_spin").hide()
}
function clearArmchair(){
    $(".arm").hide()
    $("#id_material").val("---------")
    $("#id_material").hide()
    $("#id_has_gazopatron").removeAttr("checked")
    $("#id_has_gazopatron").hide()
}
function clearCupboard(){
    $(".cup").hide()
    $("#id_quantity_of_doors").val("---------")
    $("#id_quantity_of_doors").hide()
    $("#id_has_lock").removeAttr("checked")
    $("#id_has_lock").hide()

}
function clearShelf(){
    $(".shelf").hide()
    $("#id_max_weight").val("---------")
    $("#id_max_weight").hide()

}
function clear(){
    clearArmchair()
    clearChair()
    clearCupboard()
    clearShelf()

}
function show(){
    var k=$("#id_type option:selected").val();
    if (k=="Стул"){
        clearArmchair()
        clearCupboard()
        clearShelf()
        $(".chr").show()
        $("#id_quantity_of_legs").show()
        $("#id_height_spin").show()

    }

    if (k=="Полка"){
        clearArmchair()
        clearCupboard()
        clearChair()
        $(".shelf").show()
        $("#id_max_weight").show()
    }

    if (k=="Кресло"){
        clearCupboard()
        clearChair()
        clearShelf()
        $(".arm").show()
        $("#id_material").show()
        $("#id_has_gazopatron").show()
    }

    if (k=="Шкаф"){
        clearArmchair()
        clearChair()
        clearShelf()
        $(".cup").show()
        $("#id_quantity_of_doors").show()
        $("#id_has_lock").show()
    }

    if (k=="---------"){
       clear()

    }



}


$(document).ready(function(){
    show()
			  
              $("#id_type").change(function(){
                  show()

              });
      })