const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");

socket = new WebSocket("ws://10.31.13.77:9993");

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;
    socket.send(username + " " + password);
})

socket.addEventListener("open", (e) => {
    e.preventDefault();
    console.log("connected")
  });

socket.onopen = function () {
    
};