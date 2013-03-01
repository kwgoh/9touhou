'use strict';

/* Controllers */

angular.module('app', ['ngResource']);
function FirstController($scope,$resource) {
	$scope.name = "BAKA";
	$scope.isadmin = "";
	$scope.company = "9Touhou";
	
    $scope.showdetails = false;
    $scope.apikey = "DESU";
	
	$scope.remote_url = "9touhou.appspot.com";
    $scope.waiting = "Ready";
	
	/* Login */					
	$scope.login = {};
	$scope.login.data = {"u_name":"","u_pwd":""};
	               
	$scope.getlogin = function(){
	  $scope.LoadLogin = $resource('http://:remote_url/login/login', 
					{"remote_url":$scope.remote_url},                       {'save': { method: 'POST',    params: {} }});
   
	  $scope.waiting = "Loading";
	  var login = new $scope.LoadLogin($scope.login.data);
	  login.$save(function(response) { 
			  var result = response;
			  $scope.name = result.u_name;
			  $scope.isadmin = result.u_admin;
			  $scope.waiting = "Ready";
			}); 
	};
                
	$scope.registerlogin = function(){
	  $scope.SaveLogin = $resource('http://:remote_url/login/register', 
					{"remote_url":$scope.remote_url},                       {'save': { method: 'POST',    params: {} }});
   
	  $scope.waiting = "Loading";
	  var login = new $scope.SaveLogin($scope.login.data);
	  login.$save(function(response) { 
			  var result = response;
			  $scope.name = result.u_name;
			  $scope.isadmin = result.u_admin;
			  $scope.waiting = "Ready";
			}); 
	};	

	/* Challenge (Admins) */
					
	$scope.challenge = {};
	$scope.challenge.data = {"c_name":"","c_desc":"","c_hint":"","c_points":"0","c_notes":"","c_blob":""};
	
	$scope.addchallenge = function(){
	  $scope.SaveChallenge = $resource('http://:remote_url/challenge/create', 
					{"remote_url":$scope.remote_url},                       {'save': { method: 'POST',    params: {} }});
   
	  $scope.waiting = "Loading";
	  var challenge = new $scope.SaveChallenge($scope.challenge.data);
	  challenge.$save(function(response) { 
			  var result = response;
			  $scope.listchallenge();
			  $scope.waiting = "Ready";
			}); 
	};	
 
	$scope.listchallenge = function(){
	  $scope.LoadAllChallenge = $resource('http://:remote_url/challenge/list', 
					{"remote_url":$scope.remote_url},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.LoadAllChallenge.get(function(response) { 
			  $scope.challenges = response;
			  $scope.waiting = "Ready";
			});  
	};

	$scope.listchallenge();
}

