'use strict';

angular.module('MML').controller('YearCtrl', function($scope, async, util, $routeParams, $location, moment){


    var year = +$routeParams.year;
    if(!year || year<0 || year>9999){
        // Invalid year. Go home
        $location.path('/');
    }

    $scope.year = year;
    async.api_call('GET', '/files/dates/' + $scope.year).then(function(data){
        $scope.months = data['months']
    });

    $scope.location = $location;
    $scope.date = util.date

});