var article = document.getElementById('electriccars')

c_no = article.dataset.c_no
console.log(c_no)



function call_current(){
    var current;

    $.ajax({
        url: '/call_current/',
        type: "POST",
        dataType: "json",
        data: {'send_data': c_no},
        async:false,
    
        success: function(data){
            current = data;
        }
      });

      return current;

}







	

	


