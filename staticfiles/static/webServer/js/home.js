window.onload = time; //Memulai fungsi time saat window di load

var myMap = L.map("mapDiv", {minZoom:2, maxZoom:18}).setView([-3.200000, 116.816666], 5);

// Persiapan Map
L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/dark-v9',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1Ijoic2ltYXNvbmEiLCJhIjoiY2ttbW0wNmdhMDJubTJ2cWtwOHFzN3c2YyJ9.qAEr1BRc-H_KLD0wb642ng'
}).addTo(myMap);

var oms = new OverlappingMarkerSpiderfier(myMap);

var j = 0;
for (var i = 0; i < dataResponseMatang.length; i++){
    for (j; j < dataResponse.length; j++){
        if (dataResponseMatang[i].data_mentah == dataResponse[j].id){
            dataResponse[j].suhu_udara1 = dataResponseMatang[i].suhu_udara;
            dataResponse[j].kelembaban_udara1 = dataResponseMatang[i].kelembaban_udara;
            dataResponse[j].tekanan_udara1 = dataResponseMatang[i].tekanan_udara;
            break;
        }
    }
}

var geoJSONData = dataResponse.map(function (data) {
    return {
        type: 'Feature',
        geometry: {
            type: 'Point',
            coordinates: [data.longitude, data.latitude],
        },
        properties: {
            user: {
                uuid: data.user_android.uuid,
                model: data.user_android.model,
            },
            timestamp: data.timestamp,
            lat: data.latitude,
            long: data.longitude,
            suhu_baterai: data.suhu_baterai,
            suhu_udara: data.suhu_udara,
            tekanan_udara: data.tekanan_udara,
            kelembaban_udara: data.kelembaban_udara,
            suhu_udara1: data.suhu_udara1,
            tekanan_udara1: data.tekanan_udara1,
            kelembaban_udara1: data.kelembaban_udara1,
        }
    }
});

// function onEachFeature(feature, layer) {
//     // does this feature have a property named popupContent?
//     var properties = feature.properties;
//     if (properties) {
//         var popupContent = "<table class = \"table\" \"table-striped\">";
//         for (key in properties) {
//             if (key === "user") {
//                 for (item in properties.user) {
//                     popupContent += "<tr>";
//                     popupContent += "<td>" + item + "</td>";
//                     popupContent += "<td>" + properties.user[item] + "</td>";
//                     popupContent += "</tr>";
//                 };
//             }
//             if (key === 'timestamp') {
//                 var timestamp = new Date(properties[key]);
//                 popupContent += "<tr>";
//                 popupContent += "<td>" + key + "</td>";
//                 popupContent += "<td>" + timestamp + "</td>";
//                 popupContent += "</tr>";
//             };
//             if (key === "lat" || key === "long") {
//                 popupContent += "<tr>";
//                 popupContent += "<td>" + key + "</td>";
//                 popupContent += "<td>" + properties[key] + "&#176</td>";
//                 popupContent += "</tr>";
//             };
//             if (key === "suhu_udara" || key === "suhu_baterai") {
//                 popupContent += "<tr>";
//                 popupContent += "<td>" + key + "</td>";
//                 popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + " &#x2103</td>";
//                 popupContent += "</tr>";
//             };
//             if (key === "tekanan_udara") {
//                 popupContent += "<tr>";
//                 popupContent += "<td>" + key + "</td>";
//                 popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + " mmHg</td>";
//                 popupContent += "</tr>";
//             };
//             if (key === "kelembaban_udara") {
//                 popupContent += "<tr>";
//                 popupContent += "<td>" + key + "</td>";
//                 popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + "%</td>";
//                 popupContent += "</tr>";
//             };
//             if (key === "suhu_udara1") {
//                 popupContent += "<tr>";
//                 popupContent += "<td>" + key + "</td>";
//                 popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + " &#x2103</td>";
//                 popupContent += "</tr>";
//             };
//             if (key === "kelembaban_udara1") {
//                 popupContent += "<tr>";
//                 popupContent += "<td>" + key + "</td>";
//                 popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + "%</td>";
//                 popupContent += "</tr>";
//             };
//             if (key === "tekanan_udara1") {
//                 popupContent += "<tr>";
//                 popupContent += "<td>" + key + "</td>";
//                 popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + " mmHg</td>";
//                 popupContent += "</tr>";
//             };
//         };
//         popupContent += "</table>"
//     }
//     layer.bindPopup(popupContent);
// }

var mapMarker = L.Icon.extend({
    options: {
        iconSize: [40, 40],
        iconAnchor: [20, 40],
        popupAnchor: [0, -40],
    }
});

var greenIcon = new mapMarker({
    iconUrl: imageUrl + '/green.svg',
}), yellowIcon = new mapMarker({
    iconUrl: imageUrl + '/yellow.svg',
}), redIcon = new mapMarker({
    iconUrl: imageUrl + '/red.svg',
});

// L.geoJSON(geoJSONData, {
//     pointToLayer: function (feature, latlng) {
//         var timestamp = new Date(feature.properties.timestamp);
//         var now = Date.now();
//         var differTime = now - timestamp;
//         if (differTime <= twoDays) {
//             return L.marker(latlng, { icon: greenIcon });
//         }
//         else if (differTime > twoDays && differTime <= fiveDays) {
//             return L.marker(latlng, { icon: yellowIcon });
//         }
//         else {
//             return L.marker(latlng, { icon: redIcon });
//         }
//     },
//     onEachFeature: onEachFeature,

// }).addTo(myMap);

var legend = L.control({ position: "bottomleft" });
legend.onAdd = function (map) {
    var div = L.DomUtil.create("div", "legend");
    div.innerHTML += "<div class='legend-item'><img src= " + greenIcon["options"]["iconUrl"] + "> <= 2 Hari</div>";
    div.innerHTML += "<div class='legend-item'><img src= " + yellowIcon["options"]["iconUrl"] + "> 2 - 5 Hari</div>";
    div.innerHTML += "<div class='legend-item'><img src= " + redIcon["options"]["iconUrl"] + "> > 5 Hari </div>";
    return div;
};

legend.addTo(myMap);

function markerDesc(feature){
    var properties = feature.properties;
    if (properties) {
        var popupContent = "<table class = \"table\" \"table-striped\">";
        for (key in properties) {
            if (key === "user") {
                for (item in properties.user) {
                    popupContent += "<tr>";
                    popupContent += "<td>" + item + "</td>";
                    popupContent += "<td>" + properties.user[item] + "</td>";
                    popupContent += "</tr>";
                };
            }
            if (key === 'timestamp') {
                var timestamp = new Date(properties[key]);
                popupContent += "<tr>";
                popupContent += "<td>" + key + "</td>";
                popupContent += "<td>" + timestamp + "</td>";
                popupContent += "</tr>";
            };
            if (key === "lat" || key === "long") {
                popupContent += "<tr>";
                popupContent += "<td>" + key + "</td>";
                popupContent += "<td>" + properties[key] + "&#176</td>";
                popupContent += "</tr>";
            };
            if (key === "suhu_udara" || key === "suhu_baterai") {
                popupContent += "<tr>";
                popupContent += "<td>" + key + "</td>";
                popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + " &#x2103</td>";
                popupContent += "</tr>";
            };
            if (key === "tekanan_udara") {
                popupContent += "<tr>";
                popupContent += "<td>" + key + "</td>";
                popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + " mmHg</td>";
                popupContent += "</tr>";
            };
            if (key === "kelembaban_udara") {
                popupContent += "<tr>";
                popupContent += "<td>" + key + "</td>";
                popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + "%</td>";
                popupContent += "</tr>";
            };
            if (key === "suhu_udara1") {
                popupContent += "<tr>";
                popupContent += "<td>" + key + "</td>";
                popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + " &#x2103</td>";
                popupContent += "</tr>";
            };
            if (key === "kelembaban_udara1") {
                popupContent += "<tr>";
                popupContent += "<td>" + key + "</td>";
                popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + "%</td>";
                popupContent += "</tr>";
            };
            if (key === "tekanan_udara1") {
                popupContent += "<tr>";
                popupContent += "<td>" + key + "</td>";
                popupContent += "<td>" + (properties[key] == 0 ? '-' : properties[key]) + " mmHg</td>";
                popupContent += "</tr>";
            };
        };
        popupContent += "</table>"
        return popupContent;
    }
}

var popup = new L.Popup();
oms.addListener('click', function(marker) {
  popup.setContent(marker.desc);
  popup.setLatLng(marker.getLatLng());
  myMap.openPopup(popup);
});

function marker1(feature, loc){
    var timestamp = new Date(feature.properties.timestamp);
    var now = Date.now();
    var differTime = now - timestamp;
    if (differTime <= twoDays) {
        return L.marker(loc, { icon: greenIcon });
    }
    else if (differTime > twoDays && differTime <= fiveDays) {
        return L.marker(loc, { icon: yellowIcon });
    }
    else {
        return L.marker(loc, { icon: redIcon });
    }
}

oms.addListener('spiderfy', function(markers) {
    myMap.closePopup();
  });

for (var i = 0; i < geoJSONData.length; i ++) {
    var datum = geoJSONData[i];
    var loc = new L.LatLng(datum.properties.lat, datum.properties.long);
    var marker = marker1(datum, loc);
    marker.desc = markerDesc(datum);
    myMap.addLayer(marker);
    oms.addMarker(marker);  // <-- here
  }

var month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

function time() {
    var today = new Date();
    var y = today.getFullYear();
    var month1 = today.getMonth();
    var date = today.getDate();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    var timeZone = "WIB";
    if (h / 10 < 1) {
        h = "0" + h;
    }
    if (m / 10 < 1) {
        m = "0" + m;
    }
    if (s / 10 < 1) {
        s = "0" + s;
    }
    document.querySelector(".now").innerHTML = date + " " + month[month1] + " " + y + " " + h + ":" + m + ":" + s + " " + timeZone;
    setTimeout(time, 1000);
}
var x = 0;
var dataStat = document.querySelector(".dataStatistik");
dataStat.style.visibility = 'hidden';
window.addEventListener('scroll', () => {
    var limit = Math.max(document.body.scrollHeight, document.body.offsetHeight,
        document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);
    var yPos = (window.scrollY / limit) * 100;
    var yDataStat = 10;
    if (yPos >= yDataStat && x === 0) {
        dataStat.classList.add("animation");
        dataStat.style.visibility = 'visible';

    }
});