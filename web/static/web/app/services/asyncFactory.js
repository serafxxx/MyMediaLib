'use strict';


var dateRegex = /^\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d(\.\d+)?([+-][0-2]\d(:?[0-5]\d)?|Z)$/;
function parseDates(object) {
    var result = object;
    if (object != null) {
        result = angular.copy(object);
        for (var key in result) {
            var property = result[key];
            if (typeof property === 'object') {
                result[key] = parseDates(property);
            } else if (typeof property === 'string' && dateRegex.test(property)) {
                result[key] = new Date(property);
            }
        }
    }
    return result;
}

angular.module('MML')
    .factory('async', function($http, $alert){
        var promise;
        return {
            api_call: function(method, url, dataObj){
                url = '/api' + url;
                return $http({
                    method: method,
                    url: url,
                    data: dataObj,
                    params: (method === 'GET') ? dataObj : null,
                    transformResponse: function(data) {
                        try {
                            var object;
                            if (typeof data === 'object') {
                                object = data;
                            } else {
                                object = JSON.parse(data);
                            }
                            return parseDates(object);
                        } catch(e) {
                            return data;
                        }
                    }
                    // transformRequest: (method !== 'GET') ? this.transformRequest : undefined,
                    // headers: {
                    //     'Content-Type': 'application/x-www-form-urlencoded',
                    //     'X-CSRFToken': $cookies.csrftoken
                    // }
                }).then(
                    function success(response){
                        if(response.data['error']){
                            $alert({
                                title: 'API call error',
                                content: response.data['error']
                            });
                        }
                        return response.data;
                    },
                    function error(response){
                        $alert({
                            title: 'API call error',
                            content: '',
                        });
                    }
                );
            }

        }

    });


