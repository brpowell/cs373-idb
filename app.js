(function(angular) {
  'use strict';
angular.module('ngGGMate', ['ngRoute', 'ngAnimate'])
  .config(['$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider) {
      $routeProvider
        .when('/About', {
          templateUrl: 'file:///Users/Andrew/Documents/ggmate/about.html'
        })
      $locationProvider.html5Mode(true);
  }])
  .controller('MainCtrl', ['$scope', '$route', '$routeParams', '$location',
    function($scope, $route, $routeParams, $location) {
      $scope.$route = $route;
      this.$location = $location;
      this.$routeParams = $routeParams;
  }])
})(window.angular);
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/