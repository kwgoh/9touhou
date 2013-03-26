'use strict';

  var myApp = angular.module('myApp', ['ui.directives', 'ngResource']);

  myApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/view1', {templateUrl: 'partials/partial1.html', controller: FirstController});
    $routeProvider.when('/view2', {templateUrl: 'partials/partial2.html', controller: FirstController});
    $routeProvider.otherwise({redirectTo: '/view1'});
  }]);