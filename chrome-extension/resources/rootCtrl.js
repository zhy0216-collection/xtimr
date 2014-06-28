var base_url = 'http://192.168.1.3:9999/';
var request_url = {
  'getUserAnalysis' : base_url + 'get-user-type',
  'getBrowseInfo'   : base_url + 'get-browse-datetime'
};

var rootCtrl = function( $scope, $http, $q, $timeout ) {
  var fill = d3.scale.category20();
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
      },
      {
        key   : 'label-manager',
        label : '标签管理'
      }
    ],
    current_pie : '',
    current_tab : 'overview'
  };

  $scope.init = function() {
    
     var a_analysis = $http.get( request_url.getUserAnalysis );
     var a_browse = $http.get( request_url.getBrowseInfo );

     $q.all( [a_analysis, a_browse] ).then( function( values ) {
     $scope.data.analysis = values[0].data;
     $scope.data.browse = values[1].data;
     } );
    $scope.data.analysis = {
      "type"  : "\u65b0\u95fb\u8fbe\u4eba",
      "label" : [
        {"percent" : 10, "name" : "face"},
        {"percent" : 20, "name" : "than"},
        {"percent" : 30, "name" : "we"},
        {"percent" : 40, "name" : "want"},
        {"percent" : 50, "name" : "blood"},
        {"percent" : 60, "name" : "furious"},
        {"percent" : 70, "name" : "honestly"},
        {"percent" : 80, "name" : "disgrace"},
        {"percent" : 90, "name" : "rock you"},
      ]
    };
    

    $scope.initMap( $scope.data.analysis.label );
  };
  $scope.initMap = function( input ) {
    var words = [];
    for( var i = 0, len = input.length; i < len; i++ ) {
      words.push( {
        text : input[i].name,
        size : Math.round( ( input[i].percent * (1 + ( Math.round( input[i].percent / 10 ) / 10 ) ) ) / 4 ) + 12
      } );
    }

    var canvasW = 600;
    var canvasH = 600;
    var rotateCb = function() {
      return ~~(Math.random() * 2) * 90;
    };
    var fontsizeCb = function( d ) {
      return d.size;
    };

    d3.layout.cloud()
        .size( [canvasW, canvasH] )
        .words( words )
        .padding( 5 )
        .rotate( rotateCb )
        .font( "Impact" )
        .fontSize( fontsizeCb )
        .on( "end", function() {
                   d3.select( "#word-map" )
                       .append( "svg" )
                       .attr( "width", canvasW )
                       .attr( "height", canvasH )
                       .append( "g" )
                       .attr( "transform", "translate(300,300)" )
                       .selectAll( "text" )
                       .data( words )
                       .enter()
                       .append( "text" )
                       .style( "font-size", function( d ) {
                                                    return d.size + "px";
                                                  } )
                       .style( "font-family", "Impact" )
                       .style( "fill", function( d, i ) {
                                                    return fill( i );
                                                  } )
                       .attr( "text-anchor", "middle" )
                       .attr( "transform", function( d ) {
                                                   return "translate(" + [ d.x, d.y ] + ")rotate(" + d.rotate + ")";
                                                 } )
                       .text( function( d ) {
                                                   return d.text;
                                                 } );
                                                                                                                    } ).start();
  };
  $scope.initCircle = function( input, selector ) {
    var w = 300,
        h = 300,
        r = 100,
        color = d3.scale.category20c();

    var data = [];
    for( var i = 0, len = input.length; i < len; i++ ) {
      data.push( {
                   label: input[i].name,
                   value: input[i].seconds
                 } );
    }

    var vis = d3.select(selector)
        .append("svg:svg")
        .data([data])
        .attr("width", w)
        .attr("height", h)
        .append("svg:g")
        .attr("transform", "translate(" + r + "," + r + ")");

    var arc = d3.svg.arc().outerRadius(r);

    var pie = d3.layout.pie().value(function(d) { return d.value; });

    var arcs = vis.selectAll("g.slice")
        .data(pie)
        .enter()
        .append("svg:g")
        .attr("class", "slice");    //allow us to style things in the slices (like text)

    arcs.append("svg:path")
        .attr("fill", function(d, i) { return color(i); } )
        .attr("d", arc);

    arcs.append("svg:text")
        .attr("transform", function(d) {
                d.innerRadius = 0;
                d.outerRadius = r;
                return "translate(" + arc.centroid(d) + ")";
              })
        .attr("text-anchor", "middle")
        .text(function(d, i) { return data[i].label; });
  };
  $scope.switchToTab = function( key ) {
    $scope.local.current_tab = key;
  };

  $scope.init();
  $timeout( function() {
    for( var i = 0, len = $scope.data.browse.data.length; i < len; i++ ) {
      $scope.initCircle( $scope.data.browse.data[i].details, '.pie' + i );
    }
  }, 100 );
};

var app = angular.module( 'XtimrApp', [] );

app.controller( 'rootCtrl', ['$scope', '$http', '$q', '$timeout', rootCtrl] );