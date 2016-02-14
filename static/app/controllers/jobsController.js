



app.controller('JobsCtrl', function($scope, $http, Job) {

    var createJob = function ( newJob ) {
        newJob.$save();
        $scope.jobs.push( newJob );
    }

    var updateJob = function( Job ) {
        Job.$update();
    }

    $scope.showEdit = function() {
        var jb = new Job();
        jb.hour = parseInt(jb.hour);
        jb.minute = parseInt(jb.minute);

        $scope.editableJob = jb;
        $scope.isEditVisible = true;
    }

    $scope.saveJob = function( Job ) {
        $scope.isEditVisible = false;
        if ( Job.idx ) {
            updateJob( Job );
        } else {
            createJob( Job );
        }
    }

    $scope.editJob = function( Job ) {
        var jb = Job;
        jb.hour = parseInt(jb.hour);
        jb.minute = parseInt(jb.minute);

        $scope.editableJob = jb;
        $scope.isEditVisible = true;
    }

    $scope.deleteJob = function( Job ) {
        Job.$delete();
        var pos = $scope.jobs.indexOf( Job );
        $scope.jobs.splice( pos, 1 );
    }

    $scope.isEditVisible = false;
    $scope.jobs = Job.query();

});
