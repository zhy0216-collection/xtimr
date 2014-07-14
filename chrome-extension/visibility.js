// var baseUrl = chrome.storage
var start_time = new Date().getTime();

var send_time = function() {
    var data = {};
    data.start_time = start_time;
    data.end_time = new Date().getTime();
    data.total_milli_seconds = data.end_time - data.start_time;
    data.url = document.location.href;
    console.log(data);
    chrome.extension.sendMessage(data);
};

document.addEventListener("visibilitychange", function() {

    if (document.visibilityState == "visible") {
        start_time = new Date().getTime();
    } else {
        send_time();
    }


    /*
    if (document.hidden) {
        send_time();
    } else {
        if (!localStorage.start_time) {
            localStorage.start_time = new Date().getTime();
        }
    };
    */
});

window.onbeforeunload = function() {
    send_time();
}