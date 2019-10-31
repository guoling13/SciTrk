function changeClass(element) {
    // function to toggle visibility of form input fields based on search type

	if (element=="") { return }

    if (element=="location") {
    	document.getElementById('searchname').className='visible';
    	document.getElementById('searchfield').className='form';}

    if (element=="field") {
        document.getElementById('searchfield').className='visible';
        document.getElementById('searchname').className='form';}

    if (element=="family") {
        document.getElementById('searchfield').className='form';
        document.getElementById('searchname').className='visible'; }

}

// initialize map
var map;
// marker icons on map
var icons = {
      undergrad: {
        name: 'Undergrad',
        icon: 'undergrad.png'
      },
      gradStudent: {
        name: 'Grad Student',
        icon: 'gradstudent.png'
      },
      postdoc: {
        name: 'Postdoc',
        icon: 'postdoc.png'
      },
    rs: {
        name: 'Research Scientist',
        icon: 'rs.png'
      },
    collaborator: {
        name: 'Collaborator',
        icon: 'collaborator.png'
      },
    currentLoc: {
        name: 'Current Location',
        icon: 'current.png'
      },
    mixed: {
        name: 'Mixed / Others',
        icon: 'mixed.png'
      }
    };
function initMap() {
    // initialize google maps on page

    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 2,
      center: new google.maps.LatLng(25,-18),
      mapTypeId: google.maps.MapTypeId.ROADMAP
    });


    var legend = document.getElementById('legend');
    for (var key in icons) {
          var type = icons[key];
          var name = type.name;
          var icon = type.icon;
          var div = document.createElement('div');
          div.innerHTML = '<img src="' + icon + '">' + name;
          legend.appendChild(div);
        }
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(legend);
}

var markers = [];
function resultsMap(mapresults) {
    // first remove existing markers
    removeMarkers();

    // parse results into json
    if (mapresults == ']'){
        var tableDiv = document.getElementById("results_div");
        while (tableDiv.firstChild) {
            tableDiv.removeChild(tableDiv.firstChild);
        }
        var node = document.createElement("p");
        var textnode = document.createTextNode("No results found");
        node.appendChild(textnode);
        tableDiv.appendChild(node)
        return false
    }
    // parse results into json
    // preserve newlines, etc - use valid JSON
    mapresults = mapresults.replace(/\\n/g, "\\n")
               .replace(/\\'/g, "\\'")
               .replace(/\\"/g, '\\"')
               .replace(/\\&/g, "\\&")
               .replace(/\\r/g, "\\r")
               .replace(/\\t/g, "\\t")
               .replace(/\\b/g, "\\b")
               .replace(/\\f/g, "\\f")
                .replace(/\\N/g,'0');
    // remove non-printable and other non-valid JSON chars
    mapresults = mapresults.replace(/[\u0000-\u0019]+/g,"");
    var results = JSON.parse(mapresults);
    // continue only if results is not empty
    if (results.length == 0){
	return false;
	}

    // Set up marker coordinates and infowindow contents. Prevent marker overlap.
	var allLat = [];
    var allLng = [];
    var infoWindowContent = [];
    var markerLabels = [];
	for (var i=0; i <results.length; i++) {
	    var tmp1 = results[i].coords[0];
	    var tmp2 = results[i].coords[1];
	    if(allLat.includes(tmp1) && allLng[allLat.indexOf(tmp1)] == tmp2) {
	        infoWindowContent[allLat.indexOf(tmp1)] = infoWindowContent[allLat.indexOf(tmp1)] +
                    "<br><br><b>"+results[i].relation+"</b><br>"+results[i].location+"<br>"+
                results[i].name+"<br>"+results[i].years;
	        markerLabels[allLat.indexOf(tmp1)] = 'mixed';
        } else {
            allLat.push(tmp1);
            allLng.push(tmp2);
            infoWindowContent.push("<b>"+results[i].relation+"</b><br>"+results[i].location+"<br>"+
                results[i].name+"<br>"+results[i].years);
            if (results[i].relation.includes("Undergrad")) {
                markerLabels.push('undergrad');
            } else if (results[i].relation.includes("Grad student")) {
                markerLabels.push('gradStudent');
            } else if (results[i].relation.includes("Postdoc")) {
                markerLabels.push('postdoc');
            } else if (results[i].relation.includes("Research Scientist")) {
                markerLabels.push('rs');
            } else if (results[i].relation.includes("Collaborator")) {
                markerLabels.push('collaborator');
            } else if (results[i].relation.includes("Current Location")) {
                markerLabels.push('currentLoc');
            } else {
                markerLabels.push('mixed');
            }

        }
    }

    // Place markers and info windows on map
    var markerCoords = new google.maps.LatLngBounds();
    var infowindow = new google.maps.InfoWindow();
    for (var j = 0; j < allLat.length; j++) {
          var latLng = new google.maps.LatLng(allLat[j],allLng[j]);
          var marker = new google.maps.Marker({
            position: latLng,
            map: map,
              icon: icons[markerLabels[j]].icon
          });
          markers.push(marker); // keep track of markers so they can be removed later
          markerCoords.extend(latLng); // keep track of marker coords
          google.maps.event.addListener(marker, 'click', (function(marker, j) {
              return function() {
                  infowindow.setContent(infoWindowContent[j]);
                  infowindow.open(map, marker);
              }
          })(marker, j));
        }
    map.fitBounds(markerCoords); // zoom map such that markers all fit
}

function removeMarkers(){
    for (var i = 0; i < markers.length; i++){
        markers[i].setMap(null);}
    markers =[];

}

function getNameSelect() {
    var name = document.getElementById('choose_name_table').value;
    var option = document.getElementById('selectOptionSave').innerHTML;
    sendRequest(option,name);

    // Clear the old table
    var tableDiv = document.getElementById("results_div");
    while (tableDiv.firstChild) {
      tableDiv.removeChild(tableDiv.firstChild);
    }
}

function getTable() {
    // get results table
    var option = document.getElementById('searchoption').value;
    var name = document.getElementById('name').value;
    var field = document.getElementById('field').value;
    var currentInstitution = document.getElementById('currentInstitution').value;
    var distance = document.getElementById('distance').value;

    if (option==""){
    alert('Please select a search type')
        return false
    }
    else if ((option=="location" || option=="family") && name == ""){
        alert('Please insert a name')
        return false
    }
    else if (option=="field" && (field == "" || currentInstitution == "" || distance =="")){
        alert('Please fill in all boxes before submitting')
        return false
    }

    sendRequest(option,name,currentInstitution,field, distance);

    // Clear the text field
    document.getElementById('searchoption').value = "";
    document.getElementById('name').value ="";
    document.getElementById('field').value ="";
    document.getElementById('currentInstitution').value ="";
    document.getElementById('distance').value ="60";

    // Clear the old table
    var tableDiv = document.getElementById("results_div");
    while (tableDiv.firstChild) {
      tableDiv.removeChild(tableDiv.firstChild);
    }
}

function sendRequest(option,name,currentInstitution,field,distance){
  xmlhttp = new XMLHttpRequest();
  if (xmlhttp != null) {
    xmlhttp.onreadystatechange = getData; // getData is our callback method
    xmlhttp.open("GET", "cgi-bin/accessSQLDatabase.py?option="+option+"&name="+name+"&field="+field+
        "&currentInstitution="+currentInstitution+"&distance="+distance, true);
    xmlhttp.responseType = "document";
    var loadingImg = document.getElementById("loadingImg");
    loadingImg.className='visible';
    xmlhttp.send(null);
  }
}

function getData()
{
  // Are we complete?
  if (xmlhttp.readyState == 4) {
    // Yes, do we have a good http status?
    if (xmlhttp.status == 200) {
      // yes, responseXML will hold the XML document, which we can address using the DOM
      // if we only wanted the raw text, we could get xmlhttp.responseText
      var response = xmlhttp.responseXML;

      // Use the DOM to get the results table from the server
      if (response.getElementById("results_table") == null){
        var tableDiv = document.getElementById("results_div");
        while (tableDiv.firstChild) {
            tableDiv.removeChild(tableDiv.firstChild);
        }
        var node = document.createElement("p");
        var textnode = document.createTextNode("No results found");
        node.appendChild(textnode);
        tableDiv.appendChild(node)
        var loadingImg = document.getElementById("loadingImg");
        loadingImg.className='form';
        return false
      }

      var newChild = response.getElementById("results_table");
      var mapresults = response.getElementById("mapPointSave").innerHTML;
      // Get a handle on the results div
      var tableDiv = document.getElementById("results_div");

      // Add in our results table
      tableDiv.appendChild(newChild);
      resultsMap(mapresults);
      var loadingImg = document.getElementById("loadingImg");
      loadingImg.className='form';
    } else {
      alert("Unable to contact AJAX server: "+xmlhttp.status);
      var loadingImg = document.getElementById("loadingImg");
      loadingImg.className='form';
    }
  }
}
