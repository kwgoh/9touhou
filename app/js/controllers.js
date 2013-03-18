'use strict';

/* Controllers */

function FormController($scope) {
    $scope.name = "BAKA";
	$scope.isadmin = "";
    $scope.points = 0;
    
	$scope.retrievesession = function() {
		if (!localStorage.getItem('u_name') || !localStorage.getItem('u_admin') || !localStorage.getItem('u_points')) {
			localStorage.removeItem('u_name');
			localStorage.removeItem('u_admin');
			localStorage.removeItem('u_points');				
			$scope.name = "BAKA";
			$scope.isadmin = "";
            $scope.points = 0;
		} else {
			$scope.name = localStorage.getItem('u_name');
			if (localStorage.getItem('u_admin') === "true") {
				$scope.isadmin = true;
			} else {
				$scope.isadmin = false;
			}
			$scope.points = localStorage.getItem('u_points');
		}
	}
    
	$scope.retrievesession();
}

function FirstController($scope,$resource) {
	$scope.name = "BAKA";
	$scope.isadmin = "";
    $scope.points = 0;
	$scope.company = "9Touhou";
	
    $scope.showdetails = false;
    $scope.apikey = "DESU";
	
	$scope.remote_url = "9touhou.appspot.com";
    $scope.waiting = "Ready";
	
	/* Login/Users */					
	$scope.login = {};
	$scope.login.data = {"u_name":"","u_pwd":""};

	$scope.retrievesession = function() {
		if (!localStorage.getItem('u_name') || !localStorage.getItem('u_admin') || !localStorage.getItem('u_points')) {
			localStorage.removeItem('u_name');
			localStorage.removeItem('u_admin');
			localStorage.removeItem('u_points');				
			$scope.name = "BAKA";
			$scope.isadmin = "";
            $scope.points = 0;
		} else {
			$scope.name = localStorage.getItem('u_name');
			if (localStorage.getItem('u_admin') === "true") {
				$scope.isadmin = true;
			} else {
				$scope.isadmin = false;
			}
			$scope.points = localStorage.getItem('u_points');
		}
	}
	
	$scope.logout = function() {
		localStorage.removeItem('u_name');
		localStorage.removeItem('u_admin');
        localStorage.removeItem('u_points');
		$scope.name = "BAKA";
		$scope.isadmin = "";
        $scope.points = 0;
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
                $scope.points = result.u_points;
				localStorage.setItem('u_name', $scope.name);
				localStorage.setItem('u_admin', $scope.isadmin);
				localStorage.setItem('u_points', $scope.points);
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
                $scope.points = result.u_points;
				localStorage.setItem('u_name', $scope.name);
				localStorage.setItem('u_admin', $scope.isadmin);
				localStorage.setItem('u_points', $scope.points);
			  } else {
				alert(result.error);
			  }
			  $scope.login.data = {"u_name":"","u_pwd":""};
			  $scope.waiting = "Ready";
			}); 
	};	
 
	$scope.listusers = function(){
	  $scope.LoadAllUsers = $resource('http://:remote_url/user/list', 
					{"remote_url":$scope.remote_url},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.LoadAllUsers.get(function(response) { 
			  $scope.users = response;
			  $scope.waiting = "Ready";
			});  
	};
    
	/* Challenge (Admins) */
					
	$scope.challenge = {};
	$scope.challenge.data = {"c_name":"","c_desc":"","c_date":"","c_uploadby":"","c_songs":[],"c_notes":"","c_blob":""};
	
    $scope.c_song = {"s_name":"","s_difficulty":""};
    
    $scope.addsongtochallenge = function() {
        $scope.challenge.data.c_songs.push($scope.c_song);
        $scope.c_song = {"s_name":"","s_difficulty":""};
    }
    
    $scope.cancelchallenge = function() {
        $scope.challenge.data = {"c_name":"","c_desc":"","c_date":"","c_uploadby":"","c_songs":[],"c_notes":"","c_blob":""};    
        $scope.c_song = {"s_name":"","s_difficulty":""};
    }
    
	$scope.addchallenge = function(){
      $scope.challenge.data.c_uploadby = $scope.name;
	  $scope.SaveChallenge = $resource('http://:remote_url/challenge/create', 
					{"remote_url":$scope.remote_url},                       {'save': { method: 'POST',    params: {} }});
   
	  $scope.waiting = "Loading";
	  var challenge = new $scope.SaveChallenge($scope.challenge.data);
	  challenge.$save(function(response) { 
			  var result = response;
			  $scope.challenge.data = {"c_name":"","c_desc":"","c_date":"","c_uploadby":"","c_songs":[],"c_notes":"","c_blob":""};
			  $scope.waiting = "Ready";
			});
	  $scope.listchallenge(); 
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
	 
	$scope.deletechallenge = function(model_id){
	  $scope.DeleteChallenge = $resource('http://:remote_url/challenge/remove/:id', 
					{"remote_url":$scope.remote_url, "id":model_id},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.DeleteChallenge.get(function(response) { 
			  $scope.waiting = "Ready";
			}); 
	  $scope.listchallenge(); 
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
	
	$scope.deletesong = function(model_id){
	  $scope.DeleteSong = $resource('http://:remote_url/songdata/remove/:id', 
					{"remote_url":$scope.remote_url, "id":model_id},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.DeleteSong.get(function(response) { 
			  $scope.waiting = "Ready";
			});
	  $scope.listsongs();  
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
	 
	$scope.deletesubmission = function(model_id){
	  $scope.DeleteFile = $resource('http://:remote_url/file/remove/:id', 
					{"remote_url":$scope.remote_url, "id":model_id},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.DeleteFile.get(function(response) { 
			  $scope.waiting = "Ready";
			}); 
	  $scope.listsubmissions();
	};
    
	$scope.listsubmissions();
	$scope.retrievesession();
	$scope.listchallenge();
	$scope.listsongs();
}

