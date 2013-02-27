'use strict';

/* Controllers */

angular.module('app', ['ngResource']);
function FirstController($scope,$resource) {
   $scope.name = "BAKAs";
   $scope.company = "9Touhou";
   
   $scope.remote_url = "9touhou.appspot.com";
   

}

