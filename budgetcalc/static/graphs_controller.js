
  var $module = angular.module('ExpensesApp');
  
  $module.controller('GraphsController', ['$scope', '$log', '$http', function($scope, $log, $http) {

	  	$scope.loadData = function(){
		  	$http.post(window.location.href, {from:$scope.from, to:$scope.to}).success(function(data) {
		  		
		  		$scope.categories_color =[];
		  		$scope.expensesTotal = 0;
		  	    angular.forEach(data.expenses,function(d, k){
		  	    	$scope.expensesTotal +=d.y;
		  	    });
		  	    
		  		$scope.earningsTotal = 0;
		  	    angular.forEach(data.earnings, function(d, k){
		  	    	$scope.earningsTotal +=d.y;
		  	    });
	  			$scope.expenses =[{Key: "totaux", values:data.expenses }] ;
	  			$scope.earnings =[{Key: "totaux", values:data.earnings }] ;
	  			$log.log($scope.totals);
	  			$scope.initCharts();
		    	$scope.owner = data.owner;	    	
		  		$scope.messages = data.messages;
		  	}).error(function(data){
		  		$scope.messages = data.messages;
		  	});	
	  	};
	  	
  		$scope.initCharts = function() {
			$scope.totalsoptions = {
			    chart: {
			        type: 'discreteBarChart',
			        height: 450,
			        margin : {
			            top: 20,
			            right: 20,
			            bottom: 60,
			            left: 55
			        },
			        x: function(d){ return d.Key; },
			        y: function(d){ return d.y; },
                    color: function(d,i){
                  		return "#"+(d.data && d.data.color)
                	},
			        showValues: true,
			        valueFormat: function(d){
			            return d3.format(',.2f')(d);
			        },
			        transitionDuration: 500,
			        xAxis: {
			            axisLabel: 'Categorie'
			        },
			        yAxis: {
			            axisLabel: 'Cout',
			            axisLabelDistance: 30
			        }
			    }
			};
  		};
  		
		$scope.order = "date";
		
		var today = new Date();
		var to = new Date(today.getFullYear(), today.getMonth() + 2, 1);
		var from = new Date(today.getFullYear(), today.getMonth() + 1, 1);
		$scope.to = to.getFullYear()+"/"+to.getMonth()+"/"+to.getDate()
		$scope.from = from.getFullYear()+"/"+from.getMonth()+"/"+from.getDate()
		$scope.loadData();
		
		$scope.$watch("to", function(newValue, oldValue) {
		    $scope.loadData();
		});
		$scope.$watch("from", function(newValue, oldValue) {
		    $scope.loadData();
		});
	  	
  	}

  ]);
