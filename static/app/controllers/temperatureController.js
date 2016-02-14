
app.controller('TemperatureCtrl', function($scope, $http, $interval) {
  $scope.remoteTemperature = '??';

  this.updateTemperature = function() {
    $http({
      method: "GET",
      url : "/api/1.0/temperature/"
    }).then( function updateTemperature(response) {
      $scope.remoteTemperature = response.data;
    }, function failed() {
      $scope.remoteTemperature = '??';
    });
  }

  $interval(this.updateTemperature, 60000 );

  this.updateTemperature();
});
