
  var $module = angular.module('ExpensesApp', ['720kb.datepicker', 'nvd3', 'mp.colorPicker']);
 $(document).ready(function(){
 	$(".show_hide_sidebar").click(function(e){
 		e.preventDefault();
 		$(".sidebar").slideToggle(400);
 	});
 });
