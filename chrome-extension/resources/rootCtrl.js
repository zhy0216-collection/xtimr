var base_url = 'http://192.168.1.3:9999/';
var request_url = {
  'getUserAnalysis' : base_url + 'get-user-type',
  'getBrowseInfo'   : base_url + 'get-browse-datetime'
};
var rootCtrl = function( $scope, $http, $q ) {
  $scope.data = {
    analysis : {},
    browse   : {}
  };
  $scope.local = {
    tabs        : [
      {
        key   : 'overview',
        label : '概览'
      },
      {
        key   : 'analysis',
        label : '分析'
      }
    ],
    current_tab : 'overview'
  };

  $scope.init = function() {
    /*
    var a_analysis = $http.get( request_url.getUserAnalysis );
    var a_browse = $http.get( request_url.getBrowseInfo );

    $q.all( [a_analysis, a_browse] ).then( function( values ) {
     $scope.data.analysis = values[0].data;
     $scope.data.browse = values[1].data;
     } );*/
    $scope.data.analysis = {
      "type"  : "\u65b0\u95fb\u8fbe\u4eba",
      "label" : [
        {"percent" : 12, "name" : "label1"},
        {"percent" : 22, "name" : "label22"}
      ]
    };
    $scope.data.browse = {
      "total_time" : 100,
      "data"       : [
        {"seconds" : 30, "type" : "\u65b0\u95fb"},
        {"seconds" : 50, "type" : "\u5a31\u4e50"}
      ]
    };
  };
  $scope.switchToTab = function( key ) {
    $scope.local.current_tab = key;
  };

  $scope.init();
};

var app = angular.module( 'XtimrApp', [] );

app.controller( 'rootCtrl', ['$scope', '$http', '$q', rootCtrl] );