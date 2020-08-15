

/*
  Display boundary using missionFile coordinates
*/

export function createBoundary(missionFile) {
  // Create the script tag, set the appropriate attributes
  var script = document.createElement('script');
  script.src = 
  script.defer = true;
  script.async = true;

  var flyZonesDict = missionFile['flyZones'][0];
  var boundaryList = flyZonesDict['boundaryPoints'];
  var boundaryCoordinates = [];
  for (let dictionary of boundaryList) {
    boundaryCoordinates.push({
      lat: dictionary['latitude'],
      lng: dictionary['longitude']
    });
  }

  // Attach callback function to the `window` object
  var createMap = function() {
    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 15,
      center: {
        lat: 38.1462694444444,
        lng: -76.4281638888889
      },
      mapTypeId: 'terrain'
    });


    var flightPath = new google.maps.Polyline({
      path: boundaryCoordinates,
      geodesic: true,
      strokeColor: '#FF0000',
      strokeOpacity: 1.0,
      strokeWeight: 2

    });
    flightPath.setMap(map);
  };

  window.initMap = createMap;
  // Append the 'script' element to 'head'
  document.head.appendChild(script);

}