// send post request for logout
function logout() {
    document.getElementById("logoutForm").submit();
}

// hide navbar on scroll
let prevScrollpos = window.scrollY;
window.onscroll = function () {
    document.getElementById("navbar").style.top = (prevScrollpos > window.scrollY) ? "0" : "-60px";
    prevScrollpos = window.scrollY;
}
