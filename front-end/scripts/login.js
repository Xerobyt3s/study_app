const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");

const address = "localhost";
const port = 8001;

var socket = new WebSocket(`ws://${address}:${port}`);

var auth_status;
var username;
var password;

//Send username and password entered in html form when login button is clicked
loginButton.addEventListener("click", async (e) => {
  e.preventDefault();
  username = loginForm.username.value;
  password = loginForm.password.value;
  const event = { type: "auth", username: username, password: password };
  socket.send(JSON.stringify(event));
});
//If connected to websocket send "connection established" to websocket
socket.addEventListener("open", (e) => {
  console.log("connection established");
});
//When message is recieved it is printed to the console
socket.addEventListener("message", (e) => {
  auth_status = e.data;
  console.log(auth_status);
  if (auth_status == "completed") {
    document.cookie = `Username=Admin`
    document.cookie = `Password=Admin`
    window.location.href = "../html/main.html";
  }
});
