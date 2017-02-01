'use strict';

angular.module('MML')
    .directive('mediaList', function(util, $modal, photoFileFactory){
        return {
            restrict: 'C',
            scope:{
                mediaFiles:'=',
                groupBy: '=',
                disableMenu: '='
            },
            templateUrl: '/static/web/app/components/media/media-list.html',
            link: function($scope, element, attrs){

                $scope.selectGroupBy = 'no';
                $scope.selectGroupByIcons = [
                    {"value":"no", "label":"<i class=\"glyphicon glyphicon-th\"></i> No groupping"},
                    {"value":"by_date","label":"<i class=\"glyphicon glyphicon-calendar\"></i> By date"},
                    {"value":"by_media_type","label":"<i class=\"glyphicon glyphicon-picture\"></i> By media type"},
                ];

                if($scope.groupBy){
                    $scope.selectGroupBy = $scope.groupBy;
                }

                $scope.$watch('mediaFiles', function(){
                    updateGrouppingDicts()
                });

                $scope.onSelectGroupping = function(){
                    updateGrouppingDicts();
                };

                $scope.date = util.date;

                var updateGrouppingDicts = function(){
                    if($scope.mediaFiles){
                        if($scope.selectGroupBy == 'by_date'){
                            $scope.media_by_date = util.toByDateDict($scope.mediaFiles);
                        }else if($scope.selectGroupBy == 'by_media_type'){
                            $scope.media_by_type = util.toByTypeDict($scope.mediaFiles);
                        }
                    }
                }

            }
        }
    });