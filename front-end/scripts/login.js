const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");

socket = new WebSocket("ws://localhost:8001");

var auth_status

loginButton.addEventListener("click", async e => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;
    await socket.send("auth");
    await socket.send(username);
    await socket.send(password)

    auth_status = socket.recv()
})

socket.addEventListener("open", (e) => {
    socket.send("connection established")
  });

socket.onopen = function () {
    
};