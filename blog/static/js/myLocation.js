function initMap(){
	map = new google.maps.Map(document.getElementById('dispmap'),{
		center : {lat:-34.397, lng:150.644},
		zoom: 6,
	});

	//var map = new google.maps.Map(document.getElementById())

	
	infoWindow = new google.maps.InfoWindow;

	if(navigator.geolocation){
		navigator.geolocation.getCurrentPosition(function(position){
			var pos = {
				lat: position.coords.latitude,
				lng: position.coords.longitude
			};
			infoWindow.setPosition(pos);
			infoWindow.setContent("You");
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
