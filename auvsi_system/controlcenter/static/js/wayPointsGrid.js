/*
  Display Search Grid using missionFile coordinates
*/

export function createWayPointsGrid(missionFile) {
    // Create the script tag, set the appropriate attributes
    var script = document.createElement('script');
    script.src = 
    script.defer = true;
    script.async = true;
  
    var wayPointList = missionFile['waypoints'];
      var wayPointsCoordinates = [];
      for (let dictionary of wayPointList) {
        wayPointsCoordinates.push({
          lat: dictionary['latitude'],
          lng: dictionary['longitude']
        }
        )
      }
  
    // Attach callback function to the `window` object
    var createMap = function() {
      // create map
      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 15,
        center: {lat: 38.1462694444444, lng: -76.4281638888889},
        mapTypeId: 'terrain'
      });

      // create Polyline from way point coordinates
      var flightPath = new google.maps.Polyline({
        path: wayPointsCoordinates,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2
      });

      // add a marker for each boundary coordinate
      for(let coordinate of wayPointsCoordinates){
        var marker = new google.maps.Marker({
        map: map,
        draggable: true,
        position: coordinate
        });
      }

    // event listener that calls addMarker() when the map is clicked.
    google.maps.event.addListener(map, 'click', function(event) {
      addMarker(event.latLng, map);
    });

    // hold marker that was clicked
    var selectedMarker;
    
    function addMarker(coordinate,map){
      var marker = new google.maps.Marker({
      map: map,
      draggable: true,
      position: coordinate
    });
    // add listner on the created marker
    marker.addListener('click', function update(){
                                selectedMarker = marker;
    });
  }

    // delete a selected marker
    document.getElementById("myBtn").addEventListener("click", deleteMarkers);
    function deleteMarkers(){
      selectedMarker.setMap(null);
    }

      flightPath.setMap(map);
    };
  
    window.initMap = createMap;
    // Append the 'script' element to 'head'
    document.head.appendChild(script);
  
  }