var baseUrl = 'http://192.168.1.3:9999';
// config chrome.storage;


console.log(baseUrl);

chrome.browserAction.onClicked.addListener(function(tab) {
    chrome.tabs.create({
        url: 'view.html'
    });
});


var guid = (function() {
    function s4() {
        return Math.floor((1 + Math.random()) * 0x10000)
            .toString(16)
            .substring(1);
    }
    return function() {
        return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
            s4() + '-' + s4() + s4() + s4();
    };
})();

var push_time = function(time_array) {
    var post_data = {};
    post_data.data = time_array;
    $.ajax({
        url: baseUrl + '/browse',
        method: 'post',
        headers: {
            'X-UDID': localStorage.uuid
        },
        data: {
            data: JSON.stringify(post_data)
        }
    })
        .done(function(data) {
            console.log(data);
            if (data.success) {
                console.log('上传成功');
                localStorage.fail_time = JSON.stringify([]);
            } else {
                localStorage.fail_time = JSON.stringify(post_data.data);
            }
        })
        .fail(function() {
            localStorage.fail_time = JSON.stringify(post_data.data);
        });
}

//生成uuid，假如不存在就生成，假如存在就使用

localStorage.uuid = localStorage.uuid || guid();
localStorage.fail_time = localStorage.fail_time || JSON.stringify([]);

chrome.extension.onMessage.addListener(function(data) {
    console.log("fire event")
    // console.log(data);
    // console.log(localStorage.fail_time);
    var time_array = JSON.parse(localStorage.fail_time).concat(data);
    // console.log(time_array);
    push_time(time_array);
});