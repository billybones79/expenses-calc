
  var $module = angular.module('ExpensesApp');
  
  $module.controller('ExpensesController', ['$scope', '$log', '$http', function($scope, $log, $http) {
		$scope.order = "date";
		$http.post(window.location.href, '').success(function(data) {
	  		$log.log(data);
	  		$scope.expenses = data.expenses;
	  		$scope.categories_color =[];
	  		data.categories.forEach(function(cat)
	  		{	  			
	  			$scope.categories_color[cat.name] = cat.color;
	  		});
	  		$log.log($scope.categories_color);
	  		$log.log($scope.categories);
	  		$scope.categories = data.categories;
	    	$scope.owner = data.owner;	    	
	  		$scope.messages = data.messages;
	  	}).error(function(data){
	  		$scope.messages = data.messages;
	  	});
	  
	    $scope.create = function() {
	    	var data = {'category':$scope.current_category.name, 'cost':$scope.cost, 
	    	"description":$scope.description, "date":$scope.date};
			$http.post('/'+$scope.owner.name+'/expense', data).success(function(data) {
				$log.log(data.expense);
				$scope.expenses.push(data.expense);
				
			})
		};
		$scope.destroy = function($expense){
			
			$http.delete("/"+$scope.owner.name+'/expenses/'+$expense._id.$oid ).success(function(data) {
				
				$scope.expenses.splice($scope.expenses.indexOf($expenses), 1);
				
			})
		}


  }

  ]);
