document.addEventListener('DOMContentLoaded', () => {
  const errorsNode = document.querySelector('.error');
  const socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port
  );

  socket.on('connect', () => {
    const button = document.querySelector('#sendButton');

    if (button) {
      button.onclick = () => {
        errorsNode.textContent = '';
        const inputFieldEl = document.querySelector('input');
        const message = inputFieldEl.value;
        const channel_id = inputFieldEl.dataset.channel_id;

        if (message === '') {
          errorsNode.textContent = 'Please enter a message';
        } else {
          socket.emit('message sent', {
            message,
            channel_id,
          });
        }

        inputFieldEl.value = '';
      };
    }
  });

  socket.on('messages', (data) => {
    const lastMessage = data[data.length - 1];
    const messagesNode = document.querySelector('#messages');
    const node = `
    <div>
        <p>
            <span>${lastMessage.username}</span>
            <span>${lastMessage.timestamp}</span>
        </p>
        <p>${lastMessage.content}</p>
    </div>
    `;

    messagesNode.innerHTML += node;
  });
});
