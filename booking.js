document.getElementById("showBooking").addEventListener("click", function () {
    document.getElementById("bookingSection").style.display = "block";
    document.getElementById("historySection").style.display = "none";
});

document.getElementById("showHistory").addEventListener("click", function () {
    document.getElementById("bookingSection").style.display = "none";
    document.getElementById("historySection").style.display = "block";
});