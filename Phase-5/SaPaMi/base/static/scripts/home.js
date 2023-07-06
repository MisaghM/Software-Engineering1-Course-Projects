const filterForm = document.getElementById("filterForm");
const priceMin = document.getElementById("price_min");
const priceMinText = document.getElementById("priceMinText");
const priceMax = document.getElementById("price_max");
const priceMaxText = document.getElementById("priceMaxText");

priceMin.oninput = function () {
    priceMinText.innerHTML = this.value;
}

priceMax.oninput = function () {
    priceMaxText.innerHTML = this.value;
}

function submitFiltersForm() {
    if (priceMin.valueAsNumber > priceMax.valueAsNumber) {
        alert("Minimum price cannot be higher than its max.");
        return;
    }
    filterForm.submit();
}

function clearFilters() {
    window.location.href = window.location.href.split('?')[0];
}
