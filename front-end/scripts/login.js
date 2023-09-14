const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");

const address = "localhost"
const port = 8001

var socket = new WebSocket(`ws://${address}:${port}`);

var auth_status
var username
var password

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
    const event = { type: "init",}
    socket.send(JSON.stringify(event))
  });
//When message is recieved it is printed to the console
socket.addEventListener("message", (e) => {
  auth_status = e.data
  console.log(auth_status)
  if (auth_status == "completed"){
    window.location.href = "../html/main.html"
  }
})


function transferCredentials(){
  if (auth_status == "completed"){
    return username, password
  }
}

export {transferCredentials}
