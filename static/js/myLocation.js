function initMap(){
	map = new google.maps.Map(document.getElementById('dispmap'),{
		center : {lat:12.958065, lng:80.240638},
		zoom: 6,
	});
 
	//var map = new google.maps.Map(document.getElementById())
	var marker = new google.maps.Marker({
          position: {lat:12.8489742, lng:77.6548617},
          map: map
        });
	
	infoWindow = new google.maps.InfoWindow;

	if(navigator.geolocation){
		navigator.geolocation.getCurrentPosition(function(position){
			var pos = {
				lat: position.coords.latitude,
				lng: position.coords.longitude
			};
			infoWindow.setPosition(pos);
			infoWindow.setContent("You are here !");
			infoWindow.open(map);
			map.setCenter(pos);
		},
		function(){
			handleLocationError(true, infoWindow, map.getCenter());

		});
	}
	else{
		handleLocationError(false, infoWindow, map.getCenter());
	}

	function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: Please allow website to use location.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
      }
      navigator.geolocation.getCurrentPosition(function(position){
      	loadWeather(position.coords.latitude+','+position.coords.longitude)
      });
  }


var slideIndex = 0;

function carousel() {
    var i;
    var x = document.getElementsByClassName("mySlides");
    for (i = 0; i < x.length; i++) {
      x[i].style.display = "none";
    }
    slideIndex++;
    if (slideIndex > x.length) {slideIndex = 1}
    x[slideIndex-1].style.display = "block";
    setTimeout(carousel, 2000); // Change image every 2 seconds
}


function openSegment(evt, segment){
        var i, tabcontent, tablinks;
        tabcontent = document.getElementsByClassName("tabcontent");
        for (i = 0; i < tabcontent.length; i++) {
            tabcontent[i].style.display = "none";
        }

        tablinks = document.getElementsByClassName("tablinks");
        for (i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }

        document.getElementById(segment).style.display = "block";
        evt.currentTarget.className += " active";
}

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#profilePictureDisplay').attr('src', 'url('+e.target.result +')');
            $('#profilePictureDisplay').hide();
            $('#profilePictureDisplay').fadeIn(650);
        }
        reader.readAsDataURL(input.files[0]);
    }
}

$("#profilepicture").change(function() {
    readURL(this);
});


