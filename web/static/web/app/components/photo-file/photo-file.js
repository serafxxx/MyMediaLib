'use strict';

angular.module('MML')
    .directive('photoFileThumb', function($modal, util){
        return {
            restrict: 'C',
            scope:{
                mediaFileIndex:'=',
                mediaFiles:'='
            },
            templateUrl: '/static/web/app/components/photo-file/photo-file-thumb.html',
            link: function($scope, element, attrs){
                $scope.obj = $scope.mediaFiles[$scope.mediaFileIndex];

                var myModal = util.makeModal();
                $scope.showPhotoModal = function(){
                    util.showMediaModal(myModal, $scope.mediaFileIndex, $scope.mediaFiles);
                }
            }
        }
    })
    .directive('photoFile', function(){
        return {
            restrict: 'C',
            scope:{
                obj:'='
            },
            templateUrl: '/static/web/app/components/photo-file/photo-file.html',
            link: function($scope, element, attrs){

            }
        }
    });
