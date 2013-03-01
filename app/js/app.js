'use strict';

  //var myApp = angular.module('myApp', ['myApp.filters', 'myApp.services', 'myApp.directives','ngResource', 'analytics','ngMockE2E']);
  var myApp = angular.module('myApp', ['ngResource']);
 //var myApp = angular.module('myApp', ['ngResource','ngMockE2E']);
  
  var myApp = angular.module('myApp', ['ngResource']);

  myApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/view1', {templateUrl: 'partials/partial1.html', controller: FirstController});
    $routeProvider.when('/view2', {templateUrl: 'partials/partial2.html', controller: FirstController});
    $routeProvider.otherwise({redirectTo: '/view1'});
  }]);