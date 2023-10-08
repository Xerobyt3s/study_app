const address = "localhost";
const port = 8001;
let username = getCookie("Username");
let password = getCookie("Password");
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
console.log(`username is ${username} and password is ${password}`);

socket.addEventListener("open", (e) => {
  const event = { type: "auth", username: username, password: password };
  socket.send(JSON.stringify(event));
});

socket.addEventListener("message", (e) => {
  message = JSON.parse(e.data);
  if (message["type"] == "auth" && message["auth_status"] == false) {
    window.location.href = "../login.html";
  }
  if (message["type"] == "auth" && message["permission"] == "Admin"){
    const div = document.createElement('div');
    div.className = 'admin-btn';
    div.innerHTML = `<a href="./html/admin.html">Admin page</a>`;
    document.body.appendChild(div);
  }
});
