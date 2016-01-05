(function () {

  'use strict';

  var $module = angular.module('ExpensesApp');
  
  $module.controller('CategoriesController', ['$scope', '$log', '$http', function($scope, $log, $http) {

		$http.post(window.location.href, '').success(function(data) {
	  		$log.log(data.results);
	    	$scope.categories = data.results.categories;
	    	$scope.owner = data.results.owner[0];
	    	$scope.messages = data.messages;
	  	}).error(function(data){
	  		$scope.messages = data;
	  	});
	  
	    $scope.create = function() {
	    	var data = {'name':$scope.name, 'color':$scope.color};
			$http.post('/'+$scope.owner.name+'/category', data).success(function(data) {
				$log.log(data.results);
				$scope.categories.push(data.results);
				
			})
		};
		$scope.destroy = function($category){
			$log.log($owner);
			$http.delete('/categories/'+$category._id ).success(function(data) {
				
				$scope.categories.splice($scope.categories.indexOf($category), 1);
				
			})
		}
  }

  ]);

}());
