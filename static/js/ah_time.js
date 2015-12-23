
var remote_date = new Date();

function add_zero(val) {
    return (val < 10) ? '0' + val : val;
}

function update_time() {
    var time_ctrl = document.getElementById('time');
    if ( time_ctrl ) {
        remote_date.setTime( remote_date.getTime() + 500 );

        time_ctrl.innerHTML =
            add_zero( remote_date.getHours()) + 
            ":" + add_zero( remote_date.getMinutes()) + 
            ":" + add_zero( remote_date.getSeconds()) + 
            " " + add_zero( remote_date.getDate()) + 
            "." + add_zero( 1 + remote_date.getMonth()) + 
            "." + remote_date.getFullYear();
    }
}

function refresh_time() {
    var time_request = new XMLHttpRequest();

    time_request.onreadystatechange = function() {
        if ( time_request.readyState == 4 && time_request.status == 200 ) {
            remote_date = new Date( time_request.responseText );
        }
    }
    time_request.open('GET', '/api/1.0/time/', true);
    time_request.send();
}

var time_tracker = setInterval( refresh_time, 60000 ),
    time_updater = setInterval( update_time, 500 );

$(document).ready( function(){
    refresh_time();
});
