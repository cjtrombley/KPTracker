      let map;
      let markers = [];

      function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 43.6211955, lng: -84.6824346},
          zoom: 0
        });
          
        let locations = [
          {title: 'Michigan', location: {lat: 43.6211955, lng: -84.6824346}},
          {title: 'Luxury Lanes', location: {lat: 42.4603541, lng: -83.1256903}},
        ];

        let largeInfowindow = new google.maps.InfoWindow();
        let bounds = new google.maps.LatLngBounds();

        for (let i = 0; i < locations.length; i++) {
          let position = locations[i].location;
          let title = locations[i].title;
          let marker = new google.maps.Marker({
            map: map,
            position: position,
            title: title,
            animation: google.maps.Animation.DROP,
            id: i
          });
          markers.push(marker);
          marker.addListener('click', function() {
            populateInfoWindow(this, largeInfowindow);
          });
          bounds.extend(markers[i].position);
        }
        map.fitBounds(bounds);
      }

      function populateInfoWindow(marker, infowindow) {
        if (infowindow.marker != marker) {
          infowindow.marker = marker;
          infowindow.setContent('<div class="font-weight-bolder">' + marker.title + '</div>');
          infowindow.open(map, marker);
          infowindow.addListener('closeclick',function(){
            infowindow.setMarker = null;
          });
        }
      }