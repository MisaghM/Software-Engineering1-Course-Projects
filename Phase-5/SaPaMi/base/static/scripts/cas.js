const lformDiv = document.getElementById("lform");
const lform = document.getElementById("loginform");
const lpass = document.getElementById("loginPassword");

const sformDiv = document.getElementById("sform");
const sform = document.getElementById("signupform");
const spass = document.getElementById("signupPassword");

function showPassword(checkboxElement) {
    let x;
    if (checkboxElement.id == "loginShowPassword") {
        x = lpass;
    }
    else x = spass;

    if (checkboxElement.checked) {
        x.type = "text";
    }
    else x.type = "password";
}

function changeForms(to) {
    if (to === "signupform") {
        lformDiv.style.display = "none";
        sformDiv.style.display = "block";
        lform.reset();
        lpass.type = "password";
    }
    else if (to === "loginform") {
        sformDiv.style.display = "none";
        lformDiv.style.display = "block";
        sform.reset();
        spass.type = "password";
    }
}
