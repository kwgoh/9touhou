'use strict';

/* Controllers */

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
