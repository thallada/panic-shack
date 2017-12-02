var form = document.getElementById('say-form');
var username = document.getElementById('say-username');
var text = document.getElementById('say-text');
var send = document.getElementById('say-send');
var sending = document.getElementById('say-sending');
var success = document.getElementById('say-success');
var error = document.getElementById('say-error');

function sendChat(e) {
  e.preventDefault();

  var xhr = new XMLHttpRequest();
  var formData = new FormData(form);
  xhr.addEventListener('load', function (event) {
    console.log(event.target.responseText);
    if (event.target.status === 200) {
      error.textContent = '';
      text.value = '';
      success.style.display = 'inline-block';
    } else if (event.target.status === 422) {
      error.textContent = 'You must give a message to send! (' + event.target.status + ')';
      success.style.display = 'none';
    } else {
      error.textContent = 'Error Sending! (' + event.target.status + ')';
      success.style.display = 'none';
    }
    sending.style.display = 'none';
  });
  xhr.open('POST', '/chat/');
  xhr.send(formData);
  sending.style.display = 'inline-block';
}

form.addEventListener('submit', sendChat);
