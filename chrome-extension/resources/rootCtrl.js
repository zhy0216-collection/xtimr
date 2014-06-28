var rootCtrl = function( $scope ) {
  $scope.local = {
    tabs : [
      {
        key   : 'overview',
        label : '概览'
      },
      {
        key   : 'analysis',
        label : '分析'
      }
    ],
    current_tab: 'overview'
  };
};

var app = angular.module( 'HitourMobileApp', [] );

app.controller( 'rootCtrl', ['$scope', rootCtrl] );
console.log('hello world');