$(document).ready(function () {
        $(".delete-form").on("submit",function (event) {
           $.ajax({
               data:$(this).serialize(),
               type:'GET',
               url:'/delete_pet'
           }).done(function (data) {
               $(this).remove()
           });
           event.preventDefault()
        });

    });