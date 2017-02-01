'use strict';

angular.module('MML')
    .factory('util', function(moment, $modal, photoFileFactory, rawPhotoFactory){
        return {
            date: function(year, month, day){
                return new Date(year, month, day)
            },

            toByDateDict: function(obj_list){
                var obj_prop = 'created_date';
                var res = {};

                for(var i=0; i<obj_list.length; i++){
                    var obj = obj_list[i];
                    var year = obj[obj_prop].getFullYear();
                    var month = obj[obj_prop].getMonth() + 1;
                    var day = obj[obj_prop].getDate();

                    if(!(year in res)){
                        res[year] = {};
                    }
                    if(!(month in res[year])){
                        res[year][month] = {};
                    }
                    if(!(day in res[year][month])){
                        res[year][month][day] = [];
                    }
                    res[year][month][day].push(obj);

                }
                return res;
            },

            toByTypeDict: function(obj_list){

                var res = {};

                for(var i=0; i<obj_list.length; i++){
                    var obj = obj_list[i];

                    if(!(obj['cls'] in res)){
                        res[obj['cls']] = [];
                    }
                    res[obj['cls']].push(obj);
                }
                return res;
            },

            makeModal: function(){
                var modal = $modal({
                    // scope: $scope,
                    template: 'static/web/app/components/media/modal.html',
                    show: false,
                    animation: 'am-flip-x'
                });
                var t = this;
                modal.$scope.nextMediaFile = function(){
                    var mediaFileIndex = 0;
                    if(modal.$scope.mediaFileIndex < modal.$scope.mediaFiles.length-1){
                        mediaFileIndex = modal.$scope.mediaFileIndex + 1;
                    }
                    t.showMediaModal(modal, mediaFileIndex, modal.$scope.mediaFiles);
                };

                return modal
            },

            showMediaModal: function(modal, mediaFileIndex, mediaFiles){
                modal.$scope.mediaFiles = mediaFiles;
                modal.$scope.mediaFileIndex = mediaFileIndex;

                var obj = mediaFiles[mediaFileIndex];
                if(obj.cls == 'PhotoFile'){
                    photoFileFactory.get(obj.id).then(function(photoFile){
                        modal.$scope.currentMediaFile = photoFile;
                        modal.$promise.then(modal.show);
                    });
                }else if(obj.cls == 'RawPhoto'){
                    rawPhotoFactory.get(obj.id).then(function(rawPhoto){
                        modal.$scope.currentMediaFile = rawPhoto;
                        modal.$promise.then(modal.show);
                    });
                }
            },

            // nextMediaModal: function(modal, obj, mediaFiles){
            //     var found = false;
            //     for(var i=0; i<mediaFiles.length || found; i++){
            //
            //     }
            // }

        }

    });


