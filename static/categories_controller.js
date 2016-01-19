(function () {

  'use strict';

  var $module = angular.module('ExpensesApp');
  
  $module.controller('CategoriesController', ['$scope', '$log', '$http', function($scope, $log, $http) {

		$http.post(window.location.href, '').success(function(data) {
	  		$log.log(data);
	    	$scope.categories = data.categories;
	    	$scope.owner = data.owner;
	    	$scope.messages = data.messages;
	  	}).error(function(data){
	  		$scope.messages = data;
	  	});
	  
	    $scope.create = function() {
	    	var data = {'name':$scope.name, 'color':$scope.color};
			$http.post('/'+$scope.owner.name+'/category', data).success(function(data) {
				$log.log(data.category);
				$scope.categories.push(data.category);
				
			})
		};
		$scope.destroy = function($category){
			
			$http.delete('/'+$scope.owner.name+'/categories/'+$category._id.$oid ).success(function(data) {
				
				$scope.categories.splice($scope.categories.indexOf($category), 1);
				
			})
		}
  }

  ]);

}());
