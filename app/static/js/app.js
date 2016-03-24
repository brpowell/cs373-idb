(function(angular) {
  'use strict';
angular.module('ngGGMate', [])
  .controller('sortControllerCompanies', function($scope) {
    $scope.sortType= 'name'
    $scope.companies = [
      {name: 'Bethesda Game Studio', date_founded: 'January 01, 1986', dev: 10, pub: 0, country: "United States", html:"company1.html"},
      {name: 'Bioware', date_founded: 'Feburary 1, 1995', dev: 26, pub: 1, country: "Canada", html:"company2.html"},
      {name: 'Electronic Arts', date_founded: 'May 28, 1982', dev: 144, pub: 926, country: "United States", html:"company3.html"}

    ];
  })
  // .controller('sortControllerGames', function($scope){
  //   $scope.sortType = 'name'
  //   $scope.games = [
  //     {name}

  //   ]
  // })
})(window.angular);
/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/
