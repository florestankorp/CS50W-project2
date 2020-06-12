document.addEventListener('DOMContentLoaded', () => {
  const errorsNode = document.querySelector('.error');
  const socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port
  );

  socket.on('connect', () => {
    const button = document.querySelector('#sendButton');

    if (button) {
      button.onclick = () => {
        const inputFieldEl = document.querySelector('input');
        const message = inputFieldEl.value;
        const channel_id = inputFieldEl.dataset.channel_id;

        socket.emit('message sent', {
          message,
          channel_id,
        });
        inputFieldEl.value = '';
      };
    }
  });

  socket.on('messages', (data) => {
    const lastMessage = data[data.length - 1];
    const messagesNode = document.querySelector('#messages');
    const node = `
    <div class="message rounded-corners">
        <p class="message-info">
            <span class="message-username">${lastMessage.username}</span>
            <span class="message-timestamp">${lastMessage.timestamp}</span>
        </p>
        <p class="message-content">${lastMessage.content}</p>
    </div>`;

    messagesNode.innerHTML += node;
  });
});
