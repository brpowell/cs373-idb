var mainApp = angular.module('ngGGMate', ['ngRoute' , 'ngAnimate', 'ui.bootstrap', 'angularUtils.directives.dirPagination']);

// Routes
mainApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider
    .when('/', {
        templateUrl: '/templates/home.html'
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
    .when('/company/:id', {
        templateUrl: '/templates/company.html',
        controller: 'companyCtrl'
    })
    .when('/game/:id', {
        templateUrl: '/templates/game.html',
        controller: 'gameCtrl'
    })
    .when('/person/:id', {
        templateUrl: '/templates/person.html',
        controller: 'personCtrl'
    })
    .when('/searchResult/:searchTerm', {
        templateUrl: '/templates/searchResults.html',
        controller: 'searchCtrl'
    })
    .when('/books', {
        templateUrl: '/templates/books.html',
        controller: 'booksCtrl'
    })
    .otherwise({
        templateUrl: '/templates/home.html',
        contoller: 'homeCtrl'
    })

}]);


// Controller for company
mainApp.controller('companyCtrl', function($scope, $http, $routeParams) {
    $http.get('/api/company/' + $routeParams["id"]).then(function(result) {
        $scope.companyName = result.data['name'];
        $scope.description = result.data['deck'];
        $scope.headquarters = result.data['city'] + ', ' + result.data['country'];
        $scope.founded = result.data['date_founded']
        var p = []
        for (i in result.data['people']){
            p.push(result.data['people'][i]);
        }
        var g = []
        for (j in result.data['developed_games']) {
            g.push(result.data['developed_games'][j]);
        }
        var pubGames = []
        for (i in result.data['published_games']) {
            pubGames.push(result.data['published_games'][i]);
        }
        $scope.relatedPeople = p;
        $scope.dgames = g;
        $scope.pgames = pubGames;
        $scope.imageLink = result.data['image']
    });

    $scope.changeDate = function(str) {
        if (str) {
            return str.slice(0, 16)
        }
    };
});

// Controller for game
mainApp.controller('gameCtrl', function($scope, $http, $routeParams) {
    $http.get('/api/game/' + $routeParams["id"]).then(function(result) {
        var game = result.data
        $scope.gameName = game["name"]
        $scope.description = game['deck']
        $scope.imageLink = game["image"]
        $scope.developer = game['developers'][0]['name']
        var s = ""
        for (p in game["platforms"]) {
            s += game["platforms"][p]["name"]
            if (p < game["platforms"].length - 1) {
                s += ", "
            }
        }
        $scope.platforms = s
        $scope.cID = game['developers'][0]['id']
        $scope.publisher = game['publishers'][0]['name']
        $scope.pID = game['publishers'][0]['id']
    });
});


// Controller for person
mainApp.controller('personCtrl', function($scope, $http, $routeParams) {;
    $http.get('/api/person/' + $routeParams["id"]).then(function(result) {
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
});


// Controller for Companies
mainApp.controller('companiesListCtrl', function($scope, $http) {
    // set the default sort type
    $scope.sortType = 'name';

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

    // sorting on client side
    $scope.sort = function(key) {
        $scope.sortKey = key;
        $scope.reverse = !$scope.reverse;
    };

    $scope.getSlug = function(name) {
        return name.replace(/ /g,"_");
    };

    // changes Date Format
    $scope.changeDate = function(str) {
        return str.slice(0, 16)
    };

    // listen on resize event
    jQuery(window).resize(function() {
        hideControl();
    });

    // hide control function
    function hideControl() {
        var width = jQuery(window).width();
        if(width < 480) {
            jQuery(".dirPageLarge").hide();
            jQuery(".dirPageSmall").show();
        } else {
            jQuery(".dirPageLarge").show();
            jQuery(".dirPageSmall").hide();
        }
    }
    // trigger hide control
    hideControl();
});


// Controller for Games
mainApp.controller('gamesListCtrl', function($scope, $http) {
    // set the default sort type
    $scope.sortType = 'name';

    // total number of companies
    $scope.totalGames = 24776;

    // 20 companies per page
    $scope.gamesPerPage = 20;

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
        $http.get('/api/games/' + pageNumber).success(function(res) {
            $scope.games = res.games;
        });
    };

    // get the names from the array
    $scope.extract = function(arr) {
        var res = '';
        for (var i = 0; i < arr.length; i++) {
            res += arr[i].name;
            if(arr.length > 1 && i < arr.length - 1) {
                res += ', ';
            }
        }
        return res;
    }

    // sorting on client side
    $scope.sort = function(key) {
        $scope.sortKey = key;
        $scope.reverse = !$scope.reverse;
    }

    // changes Date Format
    $scope.changeDate = function(str) {
        return str.slice(0, 16)
    };

    // listen on resize event
    jQuery(window).resize(function() {
        hideControl();
    });

    // hide control function
    function hideControl() {
        var width = jQuery(window).width();
        if(width < 480) {
            jQuery(".dirPageLarge").hide();
            jQuery(".dirPageSmall").show();
        } else {
            jQuery(".dirPageLarge").show();
            jQuery(".dirPageSmall").hide();
        }
    }

    // trigger hide control
    hideControl();
});


// Controller for People
mainApp.controller('peopleListCtrl', function($scope, $http) {

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

    // listen on page change event
    $scope.pageChanged = function(newPage) {
        getPage(newPage);
    };

    // get a page based on the page number
    function getPage(pageNumber) {
        $http.get('/api/people/' + pageNumber).success(function(res) {
            $scope.people = res.people;
            console.log($scope.people);
        });
    };

    // sorting on client side
    $scope.sort = function(key) {
        $scope.sortKey = key;
        $scope.reverse = !$scope.reverse;
    }

    // listen on resize event
    jQuery(window).resize(function() {
        hideControl();
    });

    // hide control function
    function hideControl() {
        var width = jQuery(window).width();
        if(width < 480) {
            jQuery(".dirPageLarge").hide();
            jQuery(".dirPageSmall").show();
        } else {
            jQuery(".dirPageLarge").show();
            jQuery(".dirPageSmall").hide();
        }
    }

    // trigger hide control
    hideControl();
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


// Controller for Books
mainApp.controller('booksCtrl', function($scope, $http) {

    // section for books
    jQuery('.books-header').click(function() {
        jQuery('.books').show();
        jQuery('.authors').hide();
    });

    // section for author
    jQuery('.authors-header').click(function() {
        jQuery('.books').hide();
        jQuery('.authors').show();
    });

    // get books
    $http.get('/books').success(function(res) {
        $scope.books = res.books;
        console.log(res);
    });

    // get authors
    $http.get('/authors').success(function(res) {
        $scope.authors = res.authors;
    });

    // hide authors at the beginning
    jQuery(document).ready(function() {
        jQuery('.authors').hide();
    });  
});


// Controller for scroll
mainApp.controller('ScrollCtrl', function($scope, $location, anchorSmoothScroll) {
    $scope.gotoElement = function (eID){
      $location.hash('bottom');
      anchorSmoothScroll.scrollTo(eID);
    };
});


// Controller for about page
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


// Controller for submit
mainApp.controller('submitCtrl', function($scope, $http, $location) {
    $scope.query;
    $scope.submitQuery = function(){
        if ($scope.query) {
            $location.path("/searchResult/" + $scope.query); // path not hash
        }

    };
})


// Controller for search
mainApp.controller('searchCtrl', function($scope, $http, $routeParams) {
    var searchTerm = $routeParams["searchTerm"]
    var result
    if (searchTerm) {
        $http.get('/search', {params:{'searchbar': searchTerm}}).success(function(res) {
            $scope.games = res.games
            $scope.companies = res.companies
            $scope.people = res.people
        });
    }
});

// Controller for carousel
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
