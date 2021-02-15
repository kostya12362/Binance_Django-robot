$(function () {
  /* Functions */
  let loadForm = function () {
    let btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-order").modal("show");
      },
      success: function (data) {
        $("#modal-order .modal-content").html(data.html_form);
      }
    });
  };

  let saveForm = function () {
    let form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        console.log(data.MA);
        if (data.form_is_valid) {
          $("#order-table tbody").html(data.html_order_list);
          $("#modal-order").modal("hide");
        }
        else {
          $("#modal-order .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };
  let closeForm = function() {
        console.log("fsdfs");
        $("#modal-order").modal("hide");
    };

  /* Binding */

  // Create book
  $(".js-create-order").click(loadForm);
  $("#modal-order").on("submit", ".js-order-create-form", saveForm);
  $("#closeForm").on("submit", "#closeForm", closeForm);
});