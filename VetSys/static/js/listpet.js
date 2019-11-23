$('#search_box').keyup(function (key) {
    var key_value=key.which;
    if(key_value != ""){
        $.ajax(
            {
                url: "/search",
                data: {text:key_value},
                type: 'json',
                success: function (data) {
                	var parse="";
					for(var i=0;data.length;i++){
						var obj=data.query[i];
						parse+="<p> pet id:"+obj.id+", "+"obj name: "+ obj.name+"</p><br>";
					}
                    $('#search-result').html(parse);
                }
            }
        )
    }
    
});

function liveSearch(value){
				value = value.trim(); // remove any spaces around the text
				if(value != ""){ // don't make requests with an empty string
					$.ajax({
						url: "search",
						data: {searchText: value},
						dataType: "json",
						success: function(data){
							var res = "";
							// create the html with results
							for(i in data.results){
								res += "<div>"+data.results[i]+"</div>";
							}
							$("#results").html(res);
						}
					});
				}
				else{
					$("#results").html(""); // set the results empty in case of empty string
				}
			}