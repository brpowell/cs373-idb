'use strict';

angular.module('services', [])
	.factory('runUnitTests', function($http) {
		$http.get('/run_unittests').then(function(result){
            return result.data;
        });
	});
