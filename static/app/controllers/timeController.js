
app.controller('TimeCtrl', function($scope, $http, $interval) {
  $scope.remoteTimeValue = '';
  $scope.remoteTime = null;

  function add_zero (v) {
    return (v < 10) ? '0' + v : v;
  }

  this.updateTime = function() {
    $http({
      method: "GET",
      url : "/api/1.0/time/"
    }).then( function gotTime (response) {
        $scope.remoteTime = new Date( response.data );
    });
  }

  this.refreshTime = function() {
    if ( $scope.remoteTime ) {
      $scope.remoteTimeValue =
        add_zero( $scope.remoteTime.getHours() ) +
        ':' + add_zero($scope.remoteTime.getMinutes() ) +
        ':' + add_zero($scope.remoteTime.getSeconds() ) +
        ' ' + add_zero($scope.remoteTime.getDate() ) +
        '.' + add_zero( 1 + $scope.remoteTime.getMonth() ) +
        '.' + $scope.remoteTime.getFullYear();

      $scope.remoteTime.setTime( $scope.remoteTime.getTime() + 500 );
    }
  }
  // update time by getting it from the server
  $interval( this.updateTime, 60000 );
  $interval( this.refreshTime, 500);

  this.updateTime();

  $scope.updateRemoteTime = function() {
    var time = new Date();
    $http({
        url: "/api/1.0/time/",
        method: "POST",
        data: time.toISOString()
    }).success( function() {
        $scope.remoteTime = time;
    });
  }

});
