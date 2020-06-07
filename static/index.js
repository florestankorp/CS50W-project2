document.addEventListener('DOMContentLoaded', () => {
  const errorsNode = document.querySelector('.error');
  const socket = io.connect(
    location.protocol + '//' + document.domain + ':' + location.port
  );

  socket.on('connect', () => {
    document.querySelectorAll('button').forEach((button) => {
      button.onclick = () => {
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
    });
  });

  socket.on('messages', (data) => {
    const messagesNode = document.querySelector('#messages');
    messagesNode.appendChild(createMessageListItem(data[data.length - 1]));
  });
});

function createMessageListItem(data) {
  let list = document.createElement('div');
  let info = document.createElement('p');
  let contentItem = document.createElement('p');
  let usernameItem = document.createElement('span');
  let timestampItem = document.createElement('span');

  usernameItem.textContent = data.username;
  timestampItem.textContent = data.timestamp;
  contentItem.textContent = data.content;

  info.appendChild(usernameItem);
  info.appendChild(timestampItem);
  list.appendChild(info);
  list.appendChild(contentItem);

  return list;
}
