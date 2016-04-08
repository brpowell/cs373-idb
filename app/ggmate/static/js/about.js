var app = angular.module('about', []);
app.controller('aboutCtrl', function($scope, $http) {
	$scope.runTests = function() {
		$scope.showTestsOutput = true;
		$scope.testOutput = '\nRunning Tests ... '
		$http.get('/run_unittests').then(function(result){
			$scope.finished = true;
			$scope.testOutput = '\n' + result.data.output;
		});
	}
});