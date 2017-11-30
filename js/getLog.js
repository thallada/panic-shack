var output = document.getElementById('server-log');

function reqListener() {
  var autoScroll = document.getElementById('auto-scroll');
  output.textContent = xhr.responseText;
  if (autoScroll.checked) {
    output.scrollTop = output.scrollHeight;
  }
}

var xhr = new XMLHttpRequest();
xhr.addEventListener('load', reqListener);
xhr.open('GET', '/server.log');
xhr.send();

setInterval(function() {
  xhr = new XMLHttpRequest();
  xhr.addEventListener('load', reqListener);
  xhr.open('GET', '/server.log');
  xhr.send();
}, 10000);
