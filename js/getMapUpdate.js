var mapUpdateTime = document.getElementById('map-last-updated');

function getHeaderTime () {
  mapUpdateTime.textContent = moment(this.getResponseHeader("Last-Modified")).calendar();
}

var oReq = new XMLHttpRequest();
oReq.open("HEAD", "/map/index.html");
oReq.onload = getHeaderTime;
oReq.send();
