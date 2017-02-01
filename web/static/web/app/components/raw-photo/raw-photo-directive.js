'use strict';

angular.module('MML')
    .directive('rawPhotoThumb', function(util){
        return {
            restrict: 'C',
            scope:{
                mediaFileIndex:'=',
                mediaFiles:'='
            },
            templateUrl: '/static/web/app/components/raw-photo/raw-photo-thumb.html',
            link: function($scope, element, attrs){
                $scope.obj = $scope.mediaFiles[$scope.mediaFileIndex];

                var myModal = util.makeModal();
                $scope.showRawPhotoModal = function(){
                    util.showMediaModal(myModal, $scope.mediaFileIndex, $scope.mediaFiles);
                }
            }
        }
    })
    .directive('rawPhoto', function(){
        return {
            restrict: 'C',
            scope:{
                obj:'='
            },
            templateUrl: '/static/web/app/components/raw-photo/raw-photo.html',
            link: function(scope, element, attrs){

            }
        }
    });
