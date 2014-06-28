chrome.browserAction.onClicked.addListener(function(tab){
  chrome.tabs.create({url:'view.html'}); 
});

chrome.windows.onCreated.addListener(function(window){
  console.log(window);
});

