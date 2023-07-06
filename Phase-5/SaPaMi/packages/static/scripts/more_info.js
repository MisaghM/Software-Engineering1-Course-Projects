const rateSlider = document.getElementById("rating");
const rateText = document.getElementById("ratingText");
const userRating = '10';

document.getElementById("yourRating").innerHTML = userRating;

rateSlider.value = userRating;
rateText.innerHTML = rateSlider.value;

rateSlider.oninput = function () {
    rateText.innerHTML = this.value;
}

function rate() {
    if (rateSlider.value == userRating) {
        alert("Your rating has not changed.");
        return;
    }
    document.getElementById("rateForm").submit();
}
