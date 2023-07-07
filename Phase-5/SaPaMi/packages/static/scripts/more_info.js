const datePicker = document.getElementById("reserveDate");
datePicker.valueAsDate = new Date();
datePicker.setAttribute("min", new Date().toISOString().split("T")[0]);

const userRate = document.getElementById("yourRating").innerHTML;
const rateSlider = document.getElementById("rating");
const rateText = document.getElementById("ratingText");

rateSlider.value = (userRate == "None") ? 1 : userRate;
rateSlider.oninput = function () {
    rateText.innerHTML = this.value;
}
rateText.innerHTML = rateSlider.value;

function rate() {
    if (rateSlider.value == userRate) {
        alert("Your rating has not changed.");
        return;
    }
    document.getElementById("rateForm").submit();
}
