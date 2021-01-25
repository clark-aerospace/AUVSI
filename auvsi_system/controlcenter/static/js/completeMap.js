

/*
  Display all components of the map using missionFile coordinates
*/

export function createCompleteMap(missionFile) {
  // Create the script tag, set the appropriate attributes
  var script = document.createElement('script');
  script.src = 'https://maps.googleapis.com/maps/api/js?key=AIzaSyAHNDXWm7aUesCVL4twcs0a30ABQZpIb2A&callback=initMap';
  script.defer = true;
  script.async = true;

  var flyZonesDict = missionFile['flyZones'][0];
      
      // build boundary coordinates
      var boundaryList = flyZonesDict['boundaryPoints'];
      var boundaryCoordinates = [];
      for (let dictionary of boundaryList) {
        boundaryCoordinates.push({
          lat: dictionary['latitude'],
          lng: dictionary['longitude']
        }
        )
      }
      // build wayPoints coordinates
      var wayPointList = missionFile['waypoints'];
      var wayPointsCoordinates = [];
      for (let dictionary of wayPointList) {
        wayPointsCoordinates.push({
          lat: dictionary['latitude'],
          lng: dictionary['longitude']
        }
        )
      }

      // build search grid coordinates
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
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 15,
      center: {lat: 38.1462694444444, lng: -76.4281638888889},
      mapTypeId: 'terrain'
    });

    var boundaryPath = new google.maps.Polyline({
      path: boundaryCoordinates,
      geodesic: true,
      strokeColor: '#FF0000',
      strokeOpacity: 1.0,
      strokeWeight: 2
    });

    // create Polyline from way point coordinates
    var flightPath = new google.maps.Polyline({
      path: wayPointsCoordinates,
      geodesic: true,
      strokeColor: '#39349e',
      strokeOpacity: 1.0,
      strokeWeight: 2
    });

    // create stationary obstacles 
    var obstacleList = missionFile['stationaryObstacles'];
    for (let dictionary of obstacleList) {
      var cityCircle = new google.maps.Circle({
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: map,
        center: {lat: dictionary['latitude'], lng: dictionary['longitude']},
        radius: dictionary['radius'] / 3.2808399
      });
  }

  // create Polyline from search grid
  var searchGrid = new google.maps.Polyline({
      path: searchPointCoordinates,
      geodesic: true,
      strokeColor: '#a207fa',
      strokeOpacity: 1.0,
      strokeWeight: 2
    });

    boundaryPath.setMap(map);
    flightPath.setMap(map);
    searchGrid.setMap(map);
  };

  window.initMap = createMap;
  // Append the 'script' element to 'head'
  document.head.appendChild(script);

}