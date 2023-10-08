const address = "localhost";
const port = 8001;
let username = getCookie("Username");
let password = getCookie("Password");
var socket = new WebSocket(`ws://${address}:${port}`);
let subject = null

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

function appendNotation(array) {
  term = array[1]
  notation = array[2]
  console.log("append");
  const div = document.createElement("div");
  const notionBoard = document.querySelector('.notion-board');
  div.classList.add("notion")
  div.innerHTML = `
    <div class="notion"">
    <h3>${term}</h3>
    <strong>-</strong>
    <p>${notation}</p>
    </div>
  `;
  notionBoard.appendChild(div);
}

function createPopUp() {
  div = document.createElement("div");
  div.classList.add("popup");
  div.innerHTML = `
    <div class="popup-content">
      <h3>Skapa begrepp</h3>
      <div class="popup-input">
        <input type="text" id="term" placeholder="Term">
        <input type="text" id="notation" placeholder="Notation">
      </div>
      <div class="popup-buttons">
        <button class="cancel">Cancel</button>
        <button class="submit">Submit</button>
      </div>
    </div>
  `;
  document.body.appendChild(div);
  document.querySelector(".cancel").addEventListener("click", () => {
    document.querySelector(".popup").remove();
  });
  document.querySelector(".submit").addEventListener("click", () => {
    term = document.querySelector("#term").value;
    notation = document.querySelector("#notation").value;
    if (subject != null) {
      createNotation(term, notation, subject);
    }
    document.querySelector(".popup").remove();
  });
}

function createNotation(term, notation, subject) {
  data = {"type":"create_definition", "username": username, "word": term, "definition": notation, "subject": subject}
  socket.send(JSON.stringify(data));
}

function getNotations(subject) {
  data = {"type": "pull", "quarry": "SELECT * FROM Definitions WHERE Subject = '" + subject + "'"}
  socket.send(JSON.stringify(data));
}

function selectSubject(selectedSubject) {
  console.log(subject)
  subject = selectedSubject;
  
  // Empty the notion-board div
  document.querySelector('.notion-board').innerHTML = '';

  getNotations(subject);
}
  

//notation_message = JSON.stringify({type: "create_notation", username: username, word: word, notation: notation, subject: subject, edit_date: edit_date}
console.log(document.cookie);
console.log(`username is ${username} and password is ${password}`);

socket.addEventListener("open", (e) => {
  console.log("connected")
  const event = { type: "auth", username: username, password: password };
  socket.send(JSON.stringify(event));
});

socket.addEventListener("message", (e) => {
  message = JSON.parse(e.data);
  if (message["type"] == "auth" && message["auth_status"] == false) {
    window.location.href = "../login.html";
  }
  if (message["type"] == "answer" && message["reason"] == "quarry executed") {
    console.log(message["content"]);
    let defenitionsList = message["content"];
    for (i in defenitionsList) {
      appendNotation(defenitionsList[i]);
    }
    console.log("Quarry executed");
  }
  else if (message["type"] == "answer" && message["reason"] == "quarry failed") {
    console.log("quarry failed")
  }
});
