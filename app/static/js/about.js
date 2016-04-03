
var app = angular.module('about', []);
app.controller('aboutCtrl', function($scope, $http) {

	$scope.runTests = function() {
		$http.get('/run_unittests').then(function(result){
	        alert(1)
	        return result.data;
	    });
	}
});