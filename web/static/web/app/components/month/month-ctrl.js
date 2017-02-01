'use strict';

angular.module('MML').controller('MonthCtrl', function($scope, async, util, $routeParams, $location){

    var year = +$routeParams.year;
    var month = +$routeParams.month;
    if(!year || year<0 || year>9999){
        // Invalid year. Go home
        $location.path('/');
    }
    if(!month || month<1 || month>12){
        // Invalid month. Go home
        $location.path('/');
    }

    $scope.year = year;
    $scope.month = month;

    async.api_call('GET', '/files/dates/'+year+'/'+month).then(function(data){
        $scope.media = data['media'];
    });

    $scope.location = $location;
    $scope.date = util.date;

});