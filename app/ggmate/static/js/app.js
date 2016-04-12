var mainApp = angular.module('ngGGMate', ['ngRoute' , 'ngAnimate', 'ui.bootstrap', 'angularUtils.directives.dirPagination']);

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

mainApp.controller('companyCtrl', function($scope, $http, dataShare) {
    var id =  dataShare.getData();

    $http.get('/api/company/'.concat(id)).then(function(result) {
        $scope.companyName = result.data['name'];
        $scope.description = result.data['deck'];
        $scope.headquarters = result.data['city'];
        $scope.founded = result.data['date_founded']
        var p = []
        for (i in result.data['people']){
            p.push(result.data['people'][i]);
        }
        var g = []
        for (j in result.data['developed_games']) {
            g.push(result.data['developed_games'][j]);
        }
        $scope.relatedPeople = p;
        $scope.games = g;
        $scope.imageLink = result.data['image']
    });
    $scope.giveID = function(row) {
        dataShare.sendData(row);
        $scope.publisher = row
    };
});

mainApp.controller('gameCtrl', function($scope, $http, dataShare) {
    var id =  dataShare.getData();
    var cID;
    $http.get('/api/game/'.concat(id)).then(function(result) {
        var game = result.data
        $scope.gameName = game["name"]
        $scope.description = game['deck']
        $scope.imageLink = game["image"]
        $scope.developer = game['developers'][0]['name']
        var s = ""
        for (p in game["platforms"]) {
            if (p < game["platforms"].length)
            s += game["platforms"][p]["name"] + ", "
        }
        $scope.platforms = s
        $scope.cID = game['developers'][0]['id']
        $scope.publisher = game['publishers'][0]['name']
        $scope.pID = game['publishers'][0]['id']
    });

    $scope.giveID = function(row) {
        dataShare.sendData(row);
        $scope.publisher = row
    }

});

mainApp.controller('personCtrl', function($scope, $http, dataShare) {
    var id =  dataShare.getData();
    $http.get('/api/person/'.concat(id)).then(function(result) {
        var people = result.data
        $scope.personName = people["name"]
        $scope.description = people['deck']
        var g = []
        for (j in result.data['games']) {
            g.push(result.data['games'][j]);
        }
        $scope.games = g;
        $scope.country = people["country"]
        $scope.firstGame = people["games_created"]
    });

    $scope.giveID = function(id) {
        dataShare.sendData(row);
        $scope.publisher = row
    }
});

mainApp.controller('companiesListCtrl', function($scope, $http, dataShare) {
    // total number of companies
    $scope.totalCompanies = 617;

    // 20 companies per page        
    $scope.companiesPerPage = 20;

    // pagination       
    $scope.pagination = {
        current: 1
    };

    // get first page when load
    getPage(1);

    // listen on page change
    $scope.pageChanged = function(newPage) {
        getPage(newPage);
    };

    // get new page based on the page number
    function getPage(pageNumber) {
        $http.get('/api/companies/' + pageNumber).success(function(res) {
            $scope.companies = res.companies;
        });
    };

    // give company ID
    $scope.giveID = function(id) {
        $scope.customer = id;
        dataShare.sendData(id);
    }


    // $scope.gridOptions = {
    //     enablePaginationControls: false,
    //     paginationPageSize: 50,
    //     useExternalPagination: true
    // };
    // var paginationOptions = {
    //     pageNumber: 1,
    //     pageSize: 50,
    //     sort: null
    // };

    // var getPage = function() {
    //     var url;
    //     switch(paginationOptions.sort) {
    //       default:
    //         url = '/api/companies/'+paginationOptions.pageNumber;
    //         break;
    //     }

    //     $http.get(url).success(function (result) {
    //         $scope.gridOptions.totalItems = 617;
    //         $scope.gridOptions.data = result.companies;
    //     });

    //     $scope.gridOptions.columnDefs = [
    //         { name: 'name',
    //           cellTemplate:'<a href="#company" ng-click="grid.appScope.giveID(row)">{{COL_FIELD}}</a>', enableHiding: false },
    //         { name: 'deck', enableHiding: false },
    //         { name: 'image', enableHiding: false },
    //         { name: 'Date Founded', field: "date_founded"},
    //         { name: 'country'}
    //         ];
    //     };

    //     $scope.gridOptions.onRegisterApi = function (gridApi) {
    //         $scope.grid = gridApi;

    //         gridApi.pagination.on.paginationChanged($scope, function (newPage, pageSize) {
    //             paginationOptions.pageNumber = newPage;
    //             paginationOptions.pageSize = pageSize;
    //             getPage();
    //         });
    //     };
    // getPage();
});

mainApp.controller('gamesListCtrl', function($scope, $http, dataShare) {
    $scope.giveID = function(row) {
        $scope.customer = row.entity.id;
        dataShare.sendData(row.entity.id);
    }
    $scope.gridOptions = {
        enablePaginationControls: false,
        paginationPageSize: 50,
        useExternalPagination: true
        // useExternalSorting: true
    };
    var paginationOptions = {
        pageNumber: 1,
        pageSize: 50,
        sort: null
    };

    var getPage = function() {
        var url;
        switch(paginationOptions.sort) {
          // case uiGridConstants.ASC:
          //   url = 'https://cdn.rawgit.com/angular-ui/ui-grid.info/gh-pages/data/100_ASC.json';
          //   break;
          // case uiGridConstants.DESC:
          //   url = 'https://cdn.rawgit.com/angular-ui/ui-grid.info/gh-pages/data/100_DESC.json';
          //   break;
          default:
            url = '/api/games/'+paginationOptions.pageNumber;
            break;
        }

        $http.get(url).success(function (result) {
            $scope.gridOptions.totalItems = 24776;
            // var firstRow = (paginationOptions.pageNumber - 1) * paginationOptions.pageSize;
            // $scope.gridOptions.data = data.games.slice(firstRow, firstRow + paginationOptions.pageSize);
            // $scope.gridOptions.data = data.games
            var platforms = '';
            for (p in result.games ){
                for (q in result.games[p]['platforms']) {
                    platforms += result.games[p]['platforms'][q]['name']
                    if (q < result.games[p]['platforms'].length - 1) {
                        platforms += ', '
                    }
                }
                result.games[p]['platforms'] = platforms
                platforms = ""
            }
            $scope.gridOptions.data = result.games;
        });

        $scope.gridOptions.columnDefs = [
            { name: 'name',
              cellTemplate:'<a href="#game" ng-click="grid.appScope.giveID(row)">{{COL_FIELD}}</a>',
              enableHiding: false },
            { name: 'deck', enableHiding: false },
            { name: 'publisher', field: "publishers[0]['name']", enableHiding: false },
            { name: 'developer', field: "developers[0]['name']"},
            { name: 'platforms' }
        ];
    };

    $scope.gridOptions.onRegisterApi = function (gridApi) {
        $scope.grid = gridApi;
        gridApi.pagination.on.paginationChanged($scope, function (newPage, pageSize) {
            paginationOptions.pageNumber = newPage;
            paginationOptions.pageSize = pageSize;
            getPage();
        });
    };
    getPage();

});

mainApp.controller('peopleListCtrl', function($scope, $http, dataShare) {

    // total number of people 
    $scope.totalPeople = 72951;

    // 20 people per page
    $scope.peoplePerPage = 20;

    // pagination
    $scope.pagination = {
        current: 1
    };

    // get first page when load
    getPage(1);

    $scope.pageChanged = function(newPage) {
        getPage(newPage);
    };

    function getPage(pageNumber) {
        $http.get('/api/people/' + pageNumber).success(function(res) {
            $scope.people = res.people;
            console.log($scope.people);
        });
    };

    $scope.giveID = function(id) {
        dataShare.sendData(id);
    }

    // $scope.gridOptions = {
    //     enablePaginationControls: false,
    //     paginationPageSize: 50,
    //     useExternalPagination: true
    // };
    // var paginationOptions = {
    //     pageNumber: 1,
    //     pageSize: 50,
    //     sort: null
    // };

    // var getPage = function() {
    //     var url;
    //     switch(paginationOptions.sort) {
    //       default:
    //         url = '/api/people/'+paginationOptions.pageNumber;
    //         break;
    //     }

    //     $http.get(url).success(function (result) {
    //         $scope.gridOptions.totalItems = 72951;
    //         $scope.gridOptions.data = result.people;
    //     });

    //     $scope.gridOptions.columnDefs = [
    //         { name: 'name',
    //           cellTemplate:'<a href="#person" ng-click="grid.appScope.giveID(row)">{{COL_FIELD}}</a>',
    //           enableHiding: false },
    //         { name: 'deck', enableHiding: false },
    //         { name: 'Games Created', field: "games_created", enableHiding: false },
    //         { name: 'Country', field: "country"},
    //         { name: 'Home Town', field: "hometown" }
    //     ];
    // };

    // $scope.gridOptions.onRegisterApi = function (gridApi) {
    //     $scope.grid = gridApi;
        
    //     gridApi.pagination.on.paginationChanged($scope, function (newPage, pageSize) {
    //         paginationOptions.pageNumber = newPage;
    //         paginationOptions.pageSize = pageSize;
    //         getPage();
    //     });
    // };
    // getPage();


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
      $location.hash('bottom');
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
