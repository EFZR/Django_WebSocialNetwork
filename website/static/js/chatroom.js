const chatroom = JSON.parse(document.getElementById('chatroom').textContent);
const userName = JSON.parse(document.getElementById('user-username').textContent);
const messageInputDom = document.querySelector('#message-input');
const sendbtnDom = document.querySelector('#send-btn-input');
const chatboxDom = document.querySelector('#chat-box');

chatboxDom.scrollTop = chatboxDom.scrollHeight;

sendbtnDom.addEventListener('click', (e) => {
  e.preventDefault();
  const message = messageInputDom.value;
  socket.send(JSON.stringify({
    'message': message,
    'username': userName
  }));
  messageInputDom.value = '';
});

messageInputDom.addEventListener('click', (e) => {
  if (e.keyCode === 13) {
    e.preventDefault();
    const message = messageInputDom.value;
    socket.send(JSON.stringify({
      'message': message,
      'username': userName
    }));
    messageInputDom.value = '';
  }
});

const socket = new WebSocket(
  'ws://'
  + window.location.host
  + '/ws/chat/'
  + chatroom
  + '/'
);

socket.addEventListener('message', (e) => {
  const data = JSON.parse(e.data);
  chatboxDom.innerHTML += '<div class="card border-warning mt-3 mb-3"> <div class="card-header"> <b>' + data.username + '</b><span class="text-muted float-end">' + data.date + '</span></div><div class="card-body"><p class="card-text">' + data.message + '</p></div></div>'
  chatboxDom.scrollTop = chatboxDom.scrollHeight;
  console.log(data);
});

// Path: website\chat\consumers.py
