$('#search_box').keyup(function (key) {
    var key_value=key.which;
    if(key_value != ""){
        $.ajax({
                url: "/search_pet",
                data: {text:key_value},
                type: 'POST',
                success: function (data) {
                	var parse="";
					for(var i=0;data.length;i++){
						var obj=data.query[i];
						parse+="<p> pet id:"+obj.id+", "+"obj name: "+ obj.name+"</p><br>";
					}
                    $('#search-result').html(parse);
                }
            }
        );
    }

});
