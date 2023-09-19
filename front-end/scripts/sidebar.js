function openBtn() {
    document.getElementById("my-side-bar").style.width = "20%"
}

function closeBtn() {
    document.getElementById("my-side-bar").style.width = "0"
}

function logOut() {
    document.cookie = 'Username=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    document.cookie = 'Password=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = "../login.html";
}