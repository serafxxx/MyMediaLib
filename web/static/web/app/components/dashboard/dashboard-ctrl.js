'use strict';

angular.module('MML').controller('DashboardCtrl', function($scope, async){


    async.api_call('GET', '/files/dates').then(function(data){
        $scope.years = data['years']
    });


});