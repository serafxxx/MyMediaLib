'use strict';

angular.module('MML')
    .directive('videoFileThumb', function(){
        return {
            restrict: 'C',
            scope:{
                obj:'='
            },
            templateUrl: '/static/web/app/components/video-file/video-file-thumb.html',
            link: function(scope, element, attrs){

            }
        }
    })
    .directive('videoFile', function(){
        return {
            restrict: 'C',
            scope:{
                obj:'='
            },
            templateUrl: '/static/web/app/components/video-file/video-file.html',
            link: function(scope, element, attrs){

            }
        }
    });
