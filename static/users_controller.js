(function () {

  'use strict';

  var $module = angular.module('ExpensesApp');
  
  $module.controller('UsersController', ['$scope', '$log', '$http', function($scope, $log, $http) {

		$http.get('/owners').success(function(data) {
	  		$log.log(data.results);
	    	$scope.owners = data.results;
	  	}).error(function(data){
	  		$scope.messages = data;
	  	});
	  
	    $scope.create = function() {
	    	var data = {'name':$scope.name, 'password':$scope.password};
			$http.post('/owner', data).success(function(data) {
				$log.log(data.results);
				$scope.owners.push(data.results);
				
			})
		};
		$scope.destroy = function($owner){
			$log.log($owner);
			$http.delete('/owner/'+$owner._id ).success(function(data) {
				
				$scope.owners.splice($scope.owners.indexOf($owner), 1);
				
			})
		}
  }

  ]);

}());
