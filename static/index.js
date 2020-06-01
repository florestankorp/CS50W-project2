document.addEventListener('DOMContentLoaded', () => {
  const socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port
  );

  socket.on('connect', () => {
    document.querySelectorAll('button').forEach((button) => {
      button.onclick = () => {
        const inputFieldEl = document.querySelector('input');
        const message = inputFieldEl.value;
        const channel_id = inputFieldEl.dataset.channel_id;

        socket.emit('message sent', {
          message,
          channel_id,
        });
      };
    });
  });

  socket.on('messages', (data) => {
    console.log(data);

    data.map(({ content, username, timestamp }) => {
      console.log(content);
      console.log(username);
      console.log(timestamp);
    });

    // document.querySelector('#message').innerHTML = data.message;
  });
});
