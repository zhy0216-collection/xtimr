var baseUrl = 'http://192.168.1.3:9999';

var send_time = function(){
  var data = {};
  data.start_time = localStorage.start_time;
  data.end_time = new Date().getTime();
  data.milli_seconds = data.end_time - data.start_time;
  data.url = document.location.href;
  console.log(data);
  chrome.extension.sendMessage(data);
  localStorage.start_time = '';
};

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
