var mainApp = angular.module('ngGGMate', ['ngRoute' , 'ngAnimate', 'ui.bootstrap',
    'ui.grid', 'ui.grid.pagination']);

mainApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl: '/templates/home.html',
        controller: "CarouselDemoCtrl"
    })
    .when('/about', {
        templateUrl: '/templates/about.html',
        controller: 'aboutCtrl'
    })
    .when('/games', {
        templateUrl: '/templates/games.html',
        controller: 'gamesListCtrl'
    })
    .when('/companies', {
        templateUrl: '/templates/companies.html',
        controller: 'companiesListCtrl'
    })
    .when('/people', {
        templateUrl: '/templates/people.html',
        controller: 'peopleListCtrl'
    })
    .when('/company', {
        templateUrl: '/templates/company.html',
        controller: 'companyCtrl'
    })
    .when('/game', {
        templateUrl: '/templates/game.html',
        controller: 'gameCtrl'
    })
    .when('/person', {
        templateUrl: '/templates/person.html',
        controller: 'personCtrl'
    })
    .otherwise({
        templateUrl: '/templates/home.html'
    })

}]);

mainApp.factory('dataShare',function($rootScope){
  var service = {};
  service.data = false;
  service.sendData = function(data){
      this.data = data;
      $rootScope.$broadcast('data_shared');
  };
  service.getData = function(){
    return this.data;
  };
  return service;
});

mainApp.controller('companyCtrl', function($scope) {
    $scope.companyName = "Bungie";
    $scope.description = "This is where game description goes";
    $scope.headquarters = "This is where headquarters goes";
    $scope.founded = "This is where date founded goes";
    $scope.website = "http://ggmate.me"
    $scope.highestRated = "Highest Rated Game goes here";
    $scope.metaRating = "Metacritic rating for company";
    $scope.relatedPeople = ["Daryl Brigner", "Lani Minella",
                            "Roger L. Jackson", "Mark Jones"];
    $scope.games = ["Halo"];
    $scope.imageLink = "http://static.giantbomb.com/uploads/scale_large/1/12139/2754841-bgs.jpg";
});

mainApp.controller('gameCtrl', function($scope, $http, dataShare) {
    var id =  dataShare.getData();
    $http.get('/api/games/'.concat(id)).then(function(result) {
        var game = result.data.game[0]
        $scope.gameName = game["name"]
        $scope.description = id
    });

    // $http.get(url).then(function(result) {
    //     $scope.game = url
    //
    //     $scope.imageLink = "http://static.giantbomb.com/uploads/scale_large/8/82063/2558592-daoclean.jpg";
    //     $scope.description = $scope.text;
    //     $scope.rating = "This is where the game rating goes";
    //     $scope.platforms = "This is where the game platforms goes";
    //     $scope.developer = "This is where the game's developers goes";
    //     $scope.publisher = "This is where the game's publisher goes";
    //     $scope.people = ["Person1", "Person2", "Person3"];
    //     $scope.video = "https://www.youtube.com/embed/GE2BkLqMef4"
    // })
});

mainApp.controller('personCtrl', function($scope) {
    $scope.personName = "Peron's name goes here";
    $scope.description = "Person description goes here";
    $scope.firstGame = "Person's first credited game";
    $scope.birthDate = "Person's Birthdate";
    $scope.games = ["game1", "game2", "game3", "game4"];
});

mainApp.controller('companiesListCtrl', function($scope, gameID) {
    $scope.giveID = function(row) {
        $scope.customer = row.entity.id;
        dataShare.sendData(row.entity.id);
    }

    $scope.gridOptions = {};

    $http.get('/api/companies').then(function(result){
        $scope.gridOptions.data = result.data.companies;

        $scope.gridOptions.columnDefs = [
            { name: 'name',
              cellTemplate:'<a href="#game" target="_self">{{COL_FIELD}}</a>', enableHiding: false },
            { name: 'deck', enableHiding: false },
            { name: 'image', enableHiding: false }
            // { name: 'Date Released', enableHiding: false },
            // { name: 'Rating', enableHiding: false }
        ];
    });

    $scope.gridOptions.columnDefs = [
        { name: 'Company',
          cellTemplate:'<a href="#company" ng-click="grid.appScope.giveID(row) target="_self">{{COL_FIELD}}</a>' },
        { name: 'Date Founded'},
        { name: '# of Developed Games'},
        { name: '# of Published Games'},
        { name: 'Country' }
    ];

});

mainApp.controller('gamesListCtrl', function($scope, $http, dataShare, $rootScope) {
    $scope.giveID = function(row) {
        $scope.customer = row.entity.id;
        dataShare.sendData(row.entity.id);
    }

    $scope.gridOptions = {
        enablePaginationControls: false,
        paginationPageSize: 10
    };

    $scope.gridOptions.onRegisterApi = function (gridApi) {
        $scope.grid = gridApi;
    };

    $http.get('/api/games').then(function(result){
        $scope.gridOptions.data = result.data.games;
        $scope.gridOptions.columnDefs = [
            { name: 'name',
              cellTemplate:'<a href="#game" target="_self">{{COL_FIELD}}</a>', enableHiding: false },
            { name: 'deck', enableHiding: false },
            { name: 'image', enableHiding: false }
            // { name: 'Date Released', enableHiding: false },
            // { name: 'Rating', enableHiding: false }
        ];
    });
});

mainApp.controller('peopleListCtrl', function($scope) {
    $scope.myData = [
        {
            "Person" : "Person's name goes here",
            "Company" : "Person's company goes here",
            "First Game" : "My First Game",
            "Country" : "United States",
            "Gender" : "Male"
        }
    ]
    $scope.gridOptions = {
        enablePaginationControls: false,
        paginationPageSize: 1
    };

    $scope.gridOptions.data = $scope.myData;
    $scope.gridOptions.onRegisterApi = function (gridApi) {
        $scope.grid = gridApi;
    };
    $scope.gridOptions.columnDefs = [
        { name: 'Person',
          cellTemplate:'<a href="#game" ng-click="grid.appScope.why(row)">{{COL_FIELD}}</a>' },
        { name: 'Company'},
        { name: 'First Game'},
        { name: 'Country'},
        { name: 'Gender' }
    ];

});

// This scrolling function
// is from http://www.itnewb.com/tutorial/Creating-the-Smooth-Scroll-Effect-with-JavaScript
mainApp.service('anchorSmoothScroll', function(){
    this.scrollTo = function(eID) {
        var startY = currentYPosition();
        var stopY = elmYPosition(eID);
        var distance = stopY > startY ? stopY - startY : startY - stopY;
        if (distance < 100) {
            scrollTo(0, stopY); return;
        }
        var speed = Math.round(distance / 100);
        if (speed >= 20) speed = 10;
        var step = Math.round(distance / 25);
        var leapY = stopY > startY ? startY + step : startY - step;
        var timer = 0;
        if (stopY > startY) {
            for ( var i=startY; i<stopY; i+=step ) {
                setTimeout("window.scrollTo(0, "+leapY+")", timer * speed);
                leapY += step; if (leapY > stopY) leapY = stopY; timer++;
            } return;
        }
        for ( var i=startY; i>stopY; i-=step ) {
            setTimeout("window.scrollTo(0, "+leapY+")", timer * speed);
            leapY -= step; if (leapY < stopY) leapY = stopY; timer++;
        }

        function currentYPosition() {
            // Firefox, Chrome, Opera, Safari
            if (self.pageYOffset) return self.pageYOffset;
            // Internet Explorer 6 - standards mode
            if (document.documentElement && document.documentElement.scrollTop)
                return document.documentElement.scrollTop;
            // Internet Explorer 6, 7 and 8
            if (document.body.scrollTop) return document.body.scrollTop;
            return 0;
        }

        function elmYPosition(eID) {
            var elm = document.getElementById(eID);
            var y = elm.offsetTop;
            var node = elm;
            while (node.offsetParent && node.offsetParent != document.body) {
                node = node.offsetParent;
                y += node.offsetTop;
            } return y;
        }
    };
});

mainApp.controller('ScrollCtrl', function($scope, $location, anchorSmoothScroll) {
    $scope.gotoElement = function (eID){
      // set the location.hash to the id of
      // the element you wish to scroll to.
      $location.hash('bottom');
      // call $anchorScroll()
      anchorSmoothScroll.scrollTo(eID);
    };
});

mainApp.controller('aboutCtrl', function($scope, $http) {
    $scope.runTests = function() {
        $scope.showTestsOutput = true;
        $scope.testOutput = '\nRunning Tests ... '
        $http.get('/run_unittests').then(function(result){
            $scope.finished = true;
            $scope.testOutput = '\n' + result.data.output;
        });
    }
});

mainApp.controller('CarouselDemoCtrl', function($scope) {
    $scope.myInterval = 5000;
    $scope.noWrapSlides = false;
    $scope.active = 0;
    $scope.slides = [{image: 'http://cdn.wegotthiscovered.com/wp-content/uploads/fallout_4_14-1152x612.jpg'}, {image:
    'http://www.geforce.com/sites/default/files-world/screenshots/elder-scrolls-v-skyrim/screenshot-2.jpg'
    }];
});

/*
Copyright 2016 Google Inc. All Rights Reserved.
Use of this source code is governed by an MIT-style license that
can be found in the LICENSE file at http://angular.io/license
*/
