/*
  Display Search Grid using missionFile coordinates
*/

export function createSearchGrid(missionFile) {
    // Create the script tag, set the appropriate attributes
    var script = document.createElement('script');
    script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAHNDXWm7aUesCVL4twcs0a30ABQZpIb2A&callback=initMap';
    script.defer = true;
    script.async = true;
  
    var searchPointList = missionFile['searchGridPoints'];
      var searchPointCoordinates = [];
      for (let dictionary of searchPointList) {
        searchPointCoordinates.push({
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

      // create Polyline from search grid coordinates
      var flightPath = new google.maps.Polyline({
        path: searchPointCoordinates,
        geodesic: true,
        strokeColor: '#a207fa',
        strokeOpacity: 1.0,
        strokeWeight: 2
      });

      // add a marker for each boundary coordinate
      for(let coordinate of searchPointCoordinates){
        var marker = new google.maps.Marker({
        map: map,
        draggable: true,
        position: coordinate
        });
      }

      flightPath.setMap(map);
    };
  
    window.initMap = createMap;
    // Append the 'script' element to 'head'
    document.head.appendChild(script);
  
  }