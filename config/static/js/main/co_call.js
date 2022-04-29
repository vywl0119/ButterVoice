$.ajax({
    url: '/ajax_method/',
    type: "POST",
    dataType: "json",
    data: {'send_data': 'Send this message'},
    success: function(data){
        console.log(data);
    },beforeSend:function(){
        console.log("i am waiting");
    },complete:function(){
        console.log("i am done");
    },error: function (request, status, error) {
        console.log('i am failed');
    }
  });