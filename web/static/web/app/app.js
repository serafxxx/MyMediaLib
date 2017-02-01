'use strict';

var app = angular.module('MML', ['ngAnimate', 'ngRoute', 'mgcrea.ngStrap', 'angularMoment', 'ngSanitize'])
    .config(function ($routeProvider, $alertProvider) {
        $routeProvider
            .when('/', {
                templateUrl: 'static/web/app/components/dashboard/dashboard-view.html',
                controller: 'DashboardCtrl'
            })
            .when('/dates/:year', {
                templateUrl: 'static/web/app/components/year/year-view.html',
                controller: 'YearCtrl'
            })
            .when('/dates/:year/:month', {
                templateUrl: 'static/web/app/components/month/month-view.html',
                controller: 'MonthCtrl'
            })
            // .when('/dates/:year?/:week/:session/:exerciseId', {
            //     templateUrl: 'assets/app_user/components/exercise/exercise-view.html',
            //     controller: 'ExerciseCtrl',
            //     resolve: {
            //         Data: function (commonFactory) {
            //             return commonFactory.getAppWideData();
            //         }
            //     }
            // })
            .otherwise({
                redirectTo: '/'
            });
        angular.extend($alertProvider.defaults, {
            animation: 'am-fade-and-slide-top',
            // placement: 'top-right',
            container: '.alert-container',
            type: 'danger',
            duration: 500
        });
    })
    .run(function(amMoment) {
        amMoment.changeLocale('ru');
    });