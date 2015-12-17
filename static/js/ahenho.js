
function refresh_temperature() {
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
	if ( request.readyState == 4 && request.status == 200 ) {
	    var temp_ctrl = document.getElementById('temp_value');
	    if ( temp_ctrl ) {
            temp_ctrl.innerHTML = request.responseText;
	    }
	}
    }
    request.open('GET', '/api/1.0/temperature/', true);
    request.send();
}

// request for temperature requires a lot of time. I2C not a fastest bus
var temp_tracker = setInterval( refresh_temperature, 60000 );



$(document).ready( function(){
    refresh_temperature();
});
