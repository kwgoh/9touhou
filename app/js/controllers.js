'use strict';

/* Controllers */

/* Form Controller */

function FormController($scope) {
  $scope.name = "BAKA";
	$scope.isadmin = "";
  //$scope.points = 0;


  /* Login/Register/Session */
  
	$scope.retrievesession = function() {
		if (!localStorage.getItem('u_name') || !localStorage.getItem('u_admin') || !localStorage.getItem('u_points')) {
			localStorage.removeItem('u_name');
			localStorage.removeItem('u_admin');
			localStorage.removeItem('u_points');				
			$scope.name = "BAKA";
			$scope.isadmin = "";
      //$scope.points = 0;
		} else {
			$scope.name = localStorage.getItem('u_name');
			if (localStorage.getItem('u_admin') === "true") {
				$scope.isadmin = true;
			} else {
				$scope.isadmin = false;
			}
			//$scope.points = localStorage.getItem('u_points');
		}
	}
    
	$scope.retrievesession();
}

/* Main Controller */

function FirstController($scope,$resource) {
	$scope.name = "BAKA";
	$scope.isadmin = "";
  $scope.points = 0;
	$scope.company = "9Touhou";
	
  $scope.showdetails = false;
  $scope.apikey = "DESU";
  
  /* Marisa Special */
  
  $scope.marisa = {"mp":true,
                  "cc": true,
                  "cr": true,
                  "mr": true,
                  "mim": true,
                  "mic": true,
                  "mn": true,
                  "mm": true,
                  "mu": true,
                  "mc": true,
                  "ma": true,
                  "ms": true,
                  "vs": true,
                  "vl": true};
                  
  $scope.possible_status = ['marisa-normal',
                            'marisa-troll',
                            'marisa-sad',
                            'marisa-angry',
                            'marisa-enraged',
                            'marisa-master-spark'];
                            
  $scope.possible_progress = ['progress-danger',
                              'progress-warning',
                              'progress-success',
                              'progress-info']
                              
  $scope.nine_ball = "⑨";
  
  
  $scope.toggleNine = function() {
    
    $scope.nine_ball = $scope.nine_ball == "⑨" ? "9" : "⑨";
  }  
  
  $scope.reset = false;
  $scope.pwned = 0;
  $scope.charge = 0;
  $scope.marisa_status = $scope.possible_status[0];
  $scope.cirno_status = "cirno-normal";
  $scope.progress = $scope.possible_progress[0];
  $scope.beam_height = 0;
  
  $scope.do_troll = function(id, element) {
    $scope.beam_height = element.pageY - 250;
    var chance = Math.random();
    if (chance <= 0.25) {
      if ($scope.charge < 100) {
        var sfx = document.getElementById("yoink");
        sfx.play();
        $scope.marisa[id] = false;
        $scope.reset = true;
        
        if ($scope.charge === 0) {
          $scope.marisa_status = $scope.possible_status[1];
        }
      }
    }
  }
  
  $scope.reset_troll = function() {
    $scope.spark = false;
    var sfx = document.getElementById("splode");
    sfx.play();
    $scope.marisa = {"mp":true,
                    "cc": true,
                    "cr": true,
                    "mr": true,
                    "mim": true,
                    "mic": true,
                    "mn": true,
                    "mm": true,
                    "mu": true,
                    "mc": true,
                    "ma": true,
                    "ms": true,
                    "vs": true,
                    "vl": true};
      
    $scope.reset = false;
    $scope.pwned = $scope.pwned + 1;
    $scope.charge = $scope.charge + Math.floor(Math.random() * 11) + 5;
    
    if ($scope.charge <= 33) {
      $scope.marisa_status = $scope.possible_status[2];
    } else if ($scope.charge <= 66){
      $scope.marisa_status = $scope.possible_status[3];
      $scope.progress = $scope.possible_progress[1];
    } else if ($scope.charge <= 99){
      $scope.marisa_status = $scope.possible_status[4];
      $scope.progress = $scope.possible_progress[2];
    } else{
      var sfx = document.getElementById("charged");
      sfx.play();
      $scope.charge = 100;
      $scope.marisa_status = $scope.possible_status[5];
      $scope.progress = $scope.possible_progress[3];
    }
  }
  
  $scope.spark = false;
  
  $scope.toggle = function() {
    $scope.spark = true;
    var sfx = document.getElementById("spark");
    sfx.play();
    $scope.charge = 0;
    $scope.marisa_status = $scope.possible_status[0];
    $scope.progress = $scope.possible_progress[0];
  }
  
	$scope.remote_url = "9touhou.appspot.com";
  $scope.waiting = "Ready";

	/* Login/Users */					
	$scope.login = {};
	$scope.login.data = {"u_name":"","u_pwd":""};

	$scope.retrievesession = function() {
    $scope.VerifyLogin = $resource('http://:remote_url/user/verify', 
					{"remote_url":$scope.remote_url},{'save': { method: 'POST',    params: {} }});
		if (!localStorage.getItem('u_name') || !localStorage.getItem('u_admin') || !localStorage.getItem('u_points')) {
			localStorage.removeItem('u_name');
			localStorage.removeItem('u_admin');
			localStorage.removeItem('u_points');				
			$scope.name = "BAKA";
			$scope.isadmin = "";
      $scope.points = 0;
		} else {
      $scope.verify = {};
      $scope.verify.data = {'u_name':localStorage.getItem('u_name'),'u_admin':localStorage.getItem('u_admin')};
      $scope.waiting = "Loading";
      var v_user = new $scope.VerifyLogin($scope.verify.data);
      v_user.$save(function(response) { 
        var result = response;
        if (result.error === undefined) {
          $scope.name = result.u_name;
          $scope.isadmin = result.u_admin;
          $scope.points = result.u_points;
          localStorage.setItem('u_name', $scope.name);
          localStorage.setItem('u_admin', $scope.isadmin);
          localStorage.setItem('u_points', $scope.points);
          $scope.listnotifications();
          $scope.listachievementsusers();
          if ($scope.isadmin === true) {
            $scope.listsubmissions();
            $scope.listsongs();
            $scope.listsongssummary();
            $scope.listlogs();
          }
			  } else {
          localStorage.removeItem('u_name');
          localStorage.removeItem('u_admin');
          localStorage.removeItem('u_points');				
          $scope.name = "BAKA";
          $scope.isadmin = "";
          $scope.points = 0;
			  }
      });
		}
	}
	
	$scope.logout = function() {
		localStorage.removeItem('u_name');
		localStorage.removeItem('u_admin');
    localStorage.removeItem('u_points');
		$scope.name = "BAKA";
		$scope.isadmin = "";
    $scope.points = 0;
    window.location.replace("index.html");
	}
	
	$scope.getlogin = function(){
	  $scope.LoadLogin = $resource('http://:remote_url/login/login', 
					{"remote_url":$scope.remote_url},{'save': { method: 'POST',    params: {} }});
   
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
          $scope.listnotifications();
          $scope.listachievementsusers();
          if ($scope.isadmin === true) {
            $scope.listsubmissions();
            $scope.listsongs();
            $scope.listsongssummary();
            $scope.listlogs();
          }
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
          $scope.listnotifications();
          $scope.listachievements();
          if ($scope.isadmin === true) {
            $scope.listsubmissions();
            $scope.listsongs();
            $scope.listsongssummary();
            $scope.listlogs();
          }
			  } else {
				alert(result.error);
			  }
			  $scope.login.data = {"u_name":"","u_pwd":""};
              $scope.listusers();
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
	
  /* Filtering */
  
  $scope.userRanking = function(user) {
    return user.u_points != 0;
  }
  
  $scope.userIsAdmin = function(user) {
	return user.u_admin === "True" || user.u_admin === true;
  }
  
  $scope.userIsNotAdmin = function(user) {
	return user.u_admin === "False" || user.u_admin === false;
  }
  
  $scope.predicate_users = '-name';
  
  $scope.predicate_submissions = '-f_date';
  
  $scope.predicate_achievements = '-a_name';
  
  $scope.expireChallenge = function(chal) {
    return (new Date(chal.c_date) <= new Date());
  }
  
  $scope.activeChallenge = function(chal) {
    return (new Date(chal.c_date) > new Date());
  }
  
  $scope.half_time = function(file) {
    return (new Date(file.f_date) <= new Date('31 July 2013 23:59:59')); 
  }
  
  $scope.no_filter = function(file) {          
    return file;
  }
  
  $scope.filter = $scope.half_time;
  
  $scope.button = "Off";
  
  $scope.changeFilter = function() {
    
    $scope.filter = $scope.filter == $scope.half_time ? $scope.no_filter : $scope.half_time;
    $scope.button = $scope.button == "Off" ? "On" : "Off";
  }  
  
  /* Countdown */
  
  /* Notifications */
  
  $scope.listnotifications = function(){
	  $scope.LoadAllNotifications = $resource('http://:remote_url/notification/list/:u_name', 
					{"remote_url":$scope.remote_url,"u_name":$scope.name},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.LoadAllNotifications.get(function(response) { 
			  $scope.notifications = response;
			  $scope.waiting = "Ready";
			});  
	};
  
  /* Announcements (Admins) */
  
  /* Missions (Admins) */
  
  $scope.modules = [{"code":"CPMC10", "fullcode":"CPMC109", "title": "Introductory Arithmetics"},
                    {"code":"CPMC20", "fullcode":"CPMC209", "title": "Long Division"},
                    {"code":"CPMC30", "fullcode":"CPMC309", "title": "Introduction to Calculus"},
                    {"code":"CPMC40", "fullcode":"CPMC409", "title": "Imaginary Numbers"},
                    {"code":"CPMC50", "fullcode":"CPMC509", "title": "Basic Differentiation"},
                    {"code":"CPMC60", "fullcode":"CPMC609", "title": "Basic Integration"},
                    {"code":"CPMC70", "fullcode":"CPMC709", "title": "Introduction to Statistics"}]
                    
  $scope.newmission = [{"difficulty": "Easy", "title": "Satisfactory", "points": 4},
                    {"difficulty": "Norrmal", "title": "Merit", "points": 7},
                    {"difficulty": "Hard", "title": "Cum Laude", "points": 10},
                    {"difficulty": "Lunatic", "title": "Valedictorian", "points": 12}];
  $scope.mission = [{"difficulty": "Easy", "title": "Hand Easy", "points": 4},
                    {"difficulty": "Norrmal", "title": "Hand Normal", "points": 7},
                    {"difficulty": "Hard", "title": "Hand Hard", "points": 10},
                    {"difficulty": "Lunatic", "title": "Hand Lunatic", "points": 12}];
                    
  $scope.previous = [{"difficulty": "Easy", "title": "Menu Easy", "points": 4},
                    {"difficulty": "Norrmal", "title": "Menu Normal", "points": 7},
                    {"difficulty": "Hard", "title": "Menu Hard", "points": 10},
                    {"difficulty": "Lunatic", "title": "Menu Lunatic", "points": 12}];
	
  $scope.selected_mission = "";
  
  /* Achievement (Admins) */
  
  $scope.achievement = {};
  $scope.achievement.data = {"a_name":"","a_points":"","a_uploadby":""};
  
  $scope.awardachievement = {};
  $scope.awardachievement.data = {"a_id":"","a_user":"","a_uploadby":""};
  
  $scope.cancelachievement = function() {
    $scope.achievement.data = {"a_name":"","a_points":"","a_uploadby":""};    
  }
  
  $scope.cancelaward = function() {
    $scope.awardachievement.data = {"a_id":"","a_user":"","a_uploadby":""};  
  }
  
  $scope.listachievementsusers = function() {
    $scope.listachievements();
    $scope.listachievementawards();
    $scope.listusers();
  }
  
  $scope.addachievement = function(){
    $scope.achievement.data.a_uploadby = $scope.name;
	  $scope.SaveAchievement = $resource('http://:remote_url/achievement/create', 
					{"remote_url":$scope.remote_url},                       
          {'save': { method: 'POST',    params: {} }});
   
	  $scope.waiting = "Loading";
	  var achieve = new $scope.SaveAchievement($scope.achievement.data);
	  achieve.$save(function(response) { 
			  var result = response;
        $scope.achievement.data = {"a_name":"","a_points":"","a_uploadby":""}
        $scope.waiting = "Ready";
			});
	  $scope.listachievementsusers();
    $scope.listlogs(); 
	};	
  
  
	$scope.deleteachievement = function(model_id){
    var confirm_delete = confirm('Are you sure you want to delete this achievement?');
    if (confirm_delete == true){  
      $scope.DeleteAchievement = $resource('http://:remote_url/achievement/remove/:id', 
            {"remote_url":$scope.remote_url, "id":model_id},
            {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
            
      $scope.waiting = "Updating";       
      $scope.DeleteAchievement.get(function(response) { 
          $scope.waiting = "Ready";
        }); 
      $scope.listachievementsusers();
      $scope.listlogs();
    }
	};
  
	$scope.listachievements = function(){
	  $scope.LoadAllAchievement = $resource('http://:remote_url/achievement/list', 
					{"remote_url":$scope.remote_url},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.LoadAllAchievement.get(function(response) { 
			  $scope.achievements = response;
			  $scope.waiting = "Ready";
			});  
	};

  $scope.awardachievement = function(){
    $scope.awardachievement.data.a_uploadby = $scope.name;
	  $scope.AwardAchievement = $resource('http://:remote_url/achievement/award', 
					{"remote_url":$scope.remote_url},                       
          {'save': { method: 'POST',    params: {} }});
   
	  $scope.waiting = "Loading";
	  var awarding = new $scope.AwardAchievement($scope.awardachievement.data);
	  awarding.$save(function(response) { 
			  var result = response;
        $scope.awardachievement.data = {"a_id":"","a_user":"","a_uploadby":""};
        $scope.waiting = "Ready";
			});
    $scope.listnotifications();
	  $scope.listachievementsusers();
    $scope.listlogs(); 
	};	
  
	$scope.listachievementawards = function(){
	  $scope.LoadAllAward = $resource('http://:remote_url/achievement/listusers', 
					{"remote_url":$scope.remote_url},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.LoadAllAward.get(function(response) { 
			  $scope.achievementawards = response;
			  $scope.waiting = "Ready";
			});  
	};
  
	/* Challenge (Admins) */
					
	$scope.challenge = {};
	$scope.challenge.data = {"c_name":"","c_desc":"","c_date":"","c_uploadby":"","c_songs":[],"c_notes":"","c_blob":""};
  
  $scope.c_song = {"s_name":"","s_difficulty":""};
	
  $scope.c_scoring = {};
  $scope.c_scoring.data = {"c_id":"","c_scoreby":"","c_rankings":[]};
  
  $scope.c_ranking = {"u_name":"","u_earned":""};
  
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
    $scope.listlogs(); 
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

  $scope.addrankingtoscoring = function() {
      $scope.c_scoring.data.c_rankings.push($scope.c_ranking);
      $scope.c_ranking = {"u_name":"","u_earned":""};
  }
  
  $scope.cancelscoring = function() {
      $scope.c_scoring.data = {"c_id":"","c_scoreby":"","c_rankings":[]};
      $scope.c_ranking = {"u_name":"","u_earned":""};
  }

    
	$scope.submitscoring = function(){
    $scope.c_scoring.data.c_scoreby = $scope.name;
	  $scope.ScoreChallenge = $resource('http://:remote_url/challenge/score', 
					{"remote_url":$scope.remote_url}, 
          {'save': { method: 'POST',    params: {} }});
   
	  $scope.waiting = "Loading";
	  var c_scored = new $scope.ScoreChallenge($scope.c_scoring.data);
	  c_scored.$save(function(response) { 
			  var c_s = response;
        $scope.c_scoring.data = {"c_id":"","c_scoreby":"","c_rankings":[]};
        $scope.waiting = "Ready";
			});
	  $scope.listchallenge();
    $scope.listlogs(); 
	};	  
  
	$scope.deletechallenge = function(model_id){
    var confirm_delete = confirm('Are you sure you want to delete this challenge?');
    if (confirm_delete == true){  
      $scope.DeleteChallenge = $resource('http://:remote_url/challenge/remove/:id', 
            {"remote_url":$scope.remote_url, "id":model_id},
            {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
            
      $scope.waiting = "Updating";       
      $scope.DeleteChallenge.get(function(response) { 
          $scope.waiting = "Ready";
        }); 
      $scope.listchallenge();
      $scope.listlogs(); 
    }
	};
	
  /* Theme (Admins) */
  
	
  $scope.t_scoring = {};
  $scope.t_scoring.data = {"t_name":"","t_scoreby":"","t_rewards":[]};
  
  $scope.t_reward = {"u_name":"","u_earned":""};
  

  $scope.addrewardtotheme = function() {
      $scope.t_scoring.data.t_rewards.push($scope.t_reward);
      $scope.t_reward = {"u_name":"","u_earned":""};
  }
  
  $scope.cancelreward = function() {
      $scope.t_scoring.data = {"t_name":"","t_scoreby":"","t_rewards":[]};
      $scope.t_reward = {"u_name":"","u_earned":""};
  }

    
	$scope.submitreward = function(){
    $scope.t_scoring.data.t_scoreby = $scope.name;
	  $scope.ScoreTheme = $resource('http://:remote_url/theme/reward', 
					{"remote_url":$scope.remote_url}, 
          {'save': { method: 'POST',    params: {} }});
   
	  $scope.waiting = "Loading";
	  var t_scored = new $scope.ScoreTheme($scope.t_scoring.data);
	  t_scored.$save(function(response) { 
			  var t_s = response;
        $scope.t_scoring.data = {"t_name":"","t_scoreby":"","t_rewards":[]};
        $scope.waiting = "Ready";
			});
    $scope.listlogs(); 
	};	    
  
	/* Songs (Admins) */
	
	$scope.song = {};
	$scope.song.data = {"s_name":"","s_comp":"","s_details":"","s_uploadby":""};
	
  $scope.song_pagination = {"s_offset":0,"s_limit":10, "s_page_count": 0, "s_pages":[]};
  
  $scope.song_paginate = function(offset) {
    $scope.song_pagination.s_offset = offset;
    $scope.listsongs();
  };
  
  $scope.song_paginate_disable = function(offset) {
    return (offset === $scope.song_pagination.s_offset);
  }
  
	$scope.listsongs = function(){
    $scope.song_pagination.s_pages = [];
	  $scope.LoadAllSongs = $resource('http://:remote_url/songdata/list/:offset/:limit', 
					{"remote_url":$scope.remote_url,
          "offset":$scope.song_pagination.s_offset,
          "limit":$scope.song_pagination.s_limit},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.LoadAllSongs.get(function(response) {
			  $scope.songs = response;
        $scope.song_pagination.s_page_count = Math.ceil($scope.songs.count
                                            / $scope.song_pagination.s_limit);
        for (var p = 0; p < $scope.song_pagination.s_page_count; p++) {
          var page_no = p + 1;
          var page_off = p * $scope.song_pagination.s_limit;
          $scope.s_page = {"no": page_no,
                      "offset": page_off};
          $scope.song_pagination.s_pages.push($scope.s_page);
        }
			  $scope.waiting = "Ready";
			});  
	};
  
  $scope.listsongssummary = function() {
	  $scope.LoadSongsSummary = $resource('http://:remote_url/songdata/summarize', 
					{"remote_url":$scope.remote_url},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.LoadSongsSummary.get(function(response) {
			  $scope.songs_summary = response;
			  $scope.waiting = "Ready";
			});  
  }
	
	$scope.deletesong = function(model_id){
    var confirm_delete = confirm('Are you sure you want to delete this song?');
    if (confirm_delete == true){  
      $scope.DeleteSong = $resource('http://:remote_url/songdata/remove/:id', 
            {"remote_url":$scope.remote_url, "id":model_id},
            {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
            
      $scope.waiting = "Updating";       
      $scope.DeleteSong.get(function(response) { 
          $scope.waiting = "Ready";
        });
      $scope.listsongs();
      $scope.listsongssummary();
      $scope.listlogs(); 
    }
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
    var confirm_delete = confirm('Are you sure you want to delete this submission?');
    if (confirm_delete == true){
      $scope.DeleteFile = $resource('http://:remote_url/file/remove/:id', 
            {"remote_url":$scope.remote_url, "id":model_id},
            {'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
            
      $scope.waiting = "Updating";       
      $scope.DeleteFile.get(function(response) { 
          $scope.waiting = "Ready";
        }); 
      $scope.listnotifications();
      $scope.listsubmissions();
      $scope.listlogs();
    }
	};
    
  /* Logs (Admins) */
  
     
	$scope.listlogs = function(){
	  $scope.RecentLogs = $resource('http://:remote_url/log/list', 
					{"remote_url":$scope.remote_url},
					{'get': {method: 'JSONP', isArray: false, params:{callback: 'JSON_CALLBACK'}}});
					
	  $scope.waiting = "Updating";       
	  $scope.RecentLogs.get(function(response) { 
			  $scope.logs = response;
			  $scope.waiting = "Ready";
			});  
	}; 
    
	$scope.retrievesession();
	$scope.listchallenge();
  $scope.listusers();
}
