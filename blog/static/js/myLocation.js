function initMap(){
	map = new google.maps.Map(document.getElementById('dispmap'),{
		center : {lat:12.958065, lng:80.240638},
		zoom: 6,
	});
 
	//var map = new google.maps.Map(document.getElementById())

	var marker = new google.maps.Marker({
          position: {lat:12.958065, lng:80.240638},
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
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
        infoWindow.open(map);
      }
      navigator.geolocation.getCurrentPosition(function(position){
      	loadWeather(position.coords.latitude+','+position.coords.longitude)
      });
  }


var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";  
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
}