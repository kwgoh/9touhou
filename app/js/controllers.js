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

	$scope.retrievesession = function() {
		if (!localStorage.getItem('u_name') || !localStorage.getItem('u_admin')) {
			localStorage.removeItem('u_name');
			localStorage.removeItem('u_admin');		
			$scope.name = "BAKA";
			$scope.isadmin = "";		
		} else {
			$scope.name = localStorage.getItem('u_name');
			if (localStorage.getItem('u_admin') === "true") {
				$scope.isadmin = true;
			} else {
				$scope.isadmin = false;
			}
		}
	}
	
	$scope.logout = function() {
		localStorage.removeItem('u_name');
		localStorage.removeItem('u_admin');
		$scope.name = "BAKA";
		$scope.isadmin = "";
	}
	
	$scope.getlogin = function(){
	  $scope.LoadLogin = $resource('http://:remote_url/login/login', 
					{"remote_url":$scope.remote_url},                       {'save': { method: 'POST',    params: {} }});
   
	  $scope.waiting = "Loading";
	  var login = new $scope.LoadLogin($scope.login.data);
	  login.$save(function(response) { 
			  var result = response;
			  if (result.error === undefined) {
				$scope.name = result.u_name;
				$scope.isadmin = result.u_admin;
				localStorage.setItem('u_name', $scope.name);
				localStorage.setItem('u_admin', $scope.isadmin);
			  } else {
				alert(result.error);
			  }
			  $scope.login.data = {"u_name":"","u_pwd":""};
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
			  if (result.error === undefined) {
				$scope.name = result.u_name;
				$scope.isadmin = result.u_admin;
				localStorage.setItem('u_name', $scope.name);
				localStorage.setItem('u_admin', $scope.isadmin);
			  } else {
				alert(result.error);
			  }
			  $scope.login.data = {"u_name":"","u_pwd":""};
			  $scope.waiting = "Ready";
			}); 
	};	

	/* Challenge (Admins) */
					
	$scope.challenge = {};
	$scope.challenge.data = {"c_name":"","c_desc":"","c_date":"","c_songs":[],"c_notes":"","c_blob":""};
	
    $scope.c_song = {"s_name":"","s_difficulty":""};
    
    $scope.addsongtochallenge = function() {
        $scope.challenge.data.c_songs.push($scope.c_song);
        $scope.c_song = {"s_name":"","s_difficulty":""};
    }
    
    $scope.cancelchallenge = function() {
        $scope.challenge.data = {"c_name":"","c_desc":"","c_date":"","c_songs":[],"c_notes":"","c_blob":""};    
        $scope.c_song = {"s_name":"","s_difficulty":""};
    }
    
	$scope.addchallenge = function(){
	  $scope.SaveChallenge = $resource('http://:remote_url/challenge/create', 
					{"remote_url":$scope.remote_url},                       {'save': { method: 'POST',    params: {} }});
   
	  $scope.waiting = "Loading";
	  var challenge = new $scope.SaveChallenge($scope.challenge.data);
	  challenge.$save(function(response) { 
			  var result = response;
			  $scope.challenge.data = {"c_name":"","c_desc":"","c_date":"","c_songs":[],"c_notes":"","c_blob":""};
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
	
	/* Songs (Admins) */
	
	$scope.song = {};
	$scope.song.data = {"s_name":"","s_comp":"","s_details":"","s_uploadby":""};
	
 
	$scope.listsongs = function(){
	  $scope.LoadAllSongs = $resource('http://:remote_url/songdata/list', 
					{"remote_url":$scope.remote_url},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.LoadAllSongs.get(function(response) { 
			  $scope.songs = response;
			  $scope.waiting = "Ready";
			});  
	};
	
    /* File Submissions (Admins) */
    
	$scope.listsubmissions = function(){
	  $scope.LoadAllFiles = $resource('http://:remote_url/file/list', 
					{"remote_url":$scope.remote_url},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.LoadAllFiles.get(function(response) { 
			  $scope.blobfiles = response;
			  $scope.waiting = "Ready";
			});  
	};

	$scope.retrievesession();
	$scope.listchallenge();
	$scope.listsongs();
}

