
  var $module = angular.module('ExpensesApp');
  
  $module.controller('ChartsController', ['$scope', '$log', '$http', function($scope, $log, $http) {
		$scope.order = "date";
		$http.post(window.location.href, '').success(function(data) {
	  		
	  		$scope.categories_color =[];
	  		
  			$scope.totals =[{Key: "totaux", values:data.totals }] ;
  			$log.log($scope.totals);
  			$scope.initCharts();
	    	$scope.owner = data.owner;	    	
	  		$scope.messages = data.messages;
	  	}).error(function(data){
	  		$scope.messages = data.messages;
	  	});
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
  	}

  ]);
