const address = "localhost";
const port = 8001;
const createForm = document.getElementById("create-user-form");
const createButton = document.getElementById("create-user-form-submit");
var socket = new WebSocket(`ws://${address}:${port}`);

function getCookie(cname) {
  let name = cname + "=";
  let decodedCookie = decodeURIComponent(document.cookie);
  let clist = decodedCookie.split(";");
  for (i in clist) {
    let c = clist[i];
    while (c.charAt(0) == " ") {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}

console.log(document.cookie);

let username = getCookie("Username");
let password = getCookie("Password");
console.log(`username is ${username} and password is ${password}`);

//Send username and password entered in html form when login button is clicked
createButton.addEventListener("click", async (e) => {
  e.preventDefault();
  newUsername = createForm.username.value;
  newPassword = createForm.password.value;;
  newPermission = newPermission = createForm.permission.options[createForm.permission.selectedIndex].text;
  console.log(newPermission);
});

//If connected to websocket send "connection established" to websocket
socket.addEventListener("open", (e) => {
  console.log("connection established");
  const event = { type: "auth", username: username, password: password };
  socket.send(JSON.stringify(event));
});

//When message is recieved it is printed to the console
socket.addEventListener("message", (e) => {
  message = JSON.parse(e.data);
  if (message["type"] == "auth" && message["auth_status"] == false) {
    window.location.href = "../login.html";
  }
});
