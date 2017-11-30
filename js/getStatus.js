function getStatus() {
  MinecraftAPI.getServerStatus('panic-shack.hallada.net', {
    port: 25565
  }, function (err, status) {
    var serverError = document.getElementById('server-status-error');
    var serverStatus = document.getElementById('server-status');

    if (err) {
      serverError.style.color = 'red';
      return serverError.textContent = 'Error loading server status';
    } else {
      serverError.style.display = 'none';
    }

    serverStatus.style.display = 'block';

    if (status.online == true) {
      document.getElementById('status-online').style.display = 'inline-block';
      document.getElementById('status-offline').style.display = 'none';
    }

    document.getElementById('status-motd').textContent = status.motd;
    document.getElementById('status-players-now').textContent = status.players.now;
    document.getElementById('status-players-max').textContent = status.players.max;
    document.getElementById('status-server-name').textContent = status.server.name;
    document.getElementById('info-server-name').textContent = status.server.name;
    document.getElementById('status-server-protocol').textContent = status.server.protocol;
    document.getElementById('status-last-online').textContent = moment.unix(parseInt(status.last_online, 10)).fromNow();
    document.getElementById('status-last-updated').textContent = moment.unix(parseInt(status.last_updated, 10)).fromNow();
  });
}

getStatus();

setInterval(function () {
  getStatus();
}, 15000);
