var app = angular.module('about', []);
app.controller('aboutCtrl', function($scope, $http) {
	$scope.runTests = function() {
		$scope.showTestsOutput = true;
		$scope.testOutput = 'Running Tests ... '
		$http.get('/run_unittests').then(function(result){
			$scope.testOutput = result.data.output;
			console.log(result.data.output);
		});
	}
});