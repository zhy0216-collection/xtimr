var baseUrl = 'http://192.168.102.171:9999';

var send_time = function(){
  var data = {};
  data.start_time = localStorage.start_time;
  data.end_time = new Date().getTime();
  data.milli_seconds = data.end_time - data.start_time;
  data.url = document.location.href;
  var post_data = {};
  post_data.data = [data];

  console.log(JSON.stringify(post_data));
  $.post(baseUrl + '/broswer', {data:JSON.stringify(post_data)})
    .done(function(data){
      var data = JSON.parse(data); 
      console.log(data);
      if(data.sucessful){
        localStorage.start_time = '';
        console.log('上传成功');
      }else{
        send_time();
      }
    })
    .fail(function(){
      console.log('上传失败了，重新尝试上传');
      send_time();
    });
}

if(document.visibilityState == 'visible'){
  var start_time = new Date().getTime();
  if(!localStorage.start_time){
    localStorage.start_time = start_time;
  }
}
document.addEventListener("visibilitychange", function(){
  if(document.hidden){
    send_time();  
  }else{
    if(!localStorage.start_time){
      localStorage.start_time = new Date().getTime();
    }
  };
});

window.onbeforeunload = function(){
  send_time();
}
