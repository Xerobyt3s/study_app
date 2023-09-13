const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");

const address = "localhost"
const port = 8001

socket = new WebSocket(`ws://${address}:${port}`);

var auth_status
//Send username and password entered in html form when login button is clicked
loginButton.addEventListener("click", async e => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;
    await socket.send("auth");
    await socket.send(username);
    await socket.send(password)
})
//If connected to websocket send "connection established" to websocket
socket.addEventListener("open", (e) => {
    socket.send("connection established")
  });
//When message is recieved it is printed to the console
socket.addEventListener("message", (e) => {
  auth_status = e.data
  console.log(auth_status)
})
