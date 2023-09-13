const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");

socket = new WebSocket("ws://localhost:8000");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;
    socket.send(username + " " + password);
})

socket.addEventListener("open", (e) => {
    socket.send("connection established")
  });

socket.onopen = function () {
    
};