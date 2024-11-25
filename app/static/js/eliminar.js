 // Script para pasar el ID al modal de eliminación
 $(document).on("click", ".delete-btn", function () {
    var idCliente = $(this).data("id");
    $("#deleteForm").attr("action", "/delete/" + idCliente);
  });