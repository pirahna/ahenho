'use strict';

var app = angular
  .module('ahenho', [
    'ngResource'
  ])
  .factory('Job', function($resource){
    return $resource(
        '/api/1.0/jobs/:jobIdx/', 
        { jobIdx: '@idx' },
        { update: { method: 'PUT' }}
    );
  })
  .config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{a');
    $interpolateProvider.endSymbol('a}');
  }])
  .filter('numberFixedLen', function () {
    return function (n, len) {
        var num = parseInt(n, 10);
        len = parseInt(len, 10);
        if (isNaN(num) || isNaN(len)) {
            return n;
        }
        num = '' + num;
        while (num.length < len) {
            num = '0' + num;
        }
        return num;
    };
  });