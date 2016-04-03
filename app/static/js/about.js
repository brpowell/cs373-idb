var app = angular.module('about', []);
app.controller('aboutCtrl', function($scope, $http) {
	$scope.runTests = function() {
		$scope.testOutput = 'Running Tests ... '
		$http.get('/run_unittests').then(function(result){
			$scope.testOutput = result.data;
		});
	}
});