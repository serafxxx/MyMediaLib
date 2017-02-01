'use strict';

angular.module('MML')
    .factory('photoFileFactory', function(async){
        return {
            get: function(id){
                return async.api_call('GET', '/files/photo-files/'+id);
            }

        }

    })
    .factory('rawPhotoFactory', function(async){
        return {
            get: function(id){
                return async.api_call('GET', '/files/raw-photos/'+id);
            }

        }

    });


