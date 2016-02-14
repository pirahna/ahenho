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
  }]);