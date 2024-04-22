document.addEventListener("DOMContentLoaded", function() {
    updateTime();
    setInterval(updateTime, 1000);

    const options = ["Make an Order", "Make Reservation", "Check Reservation", "Order Stock", "Update Menu", "Payment History", "Order Management", "Edit Users", "Exit"];
    const buttonContainer = document.getElementById("button-container");

    options.forEach(option => {
        const button = document.createElement("button");
        button.textContent = option;
        button.onclick = () => openOptionWindow(option);
        buttonContainer.appendChild(button);
    });
});

function updateTime() {
    const now = new Date();
    const datetimeElement = document.getElementById("datetime");
    datetimeElement.textContent = now.toLocaleString();
}

function openOptionWindow(option) {
    switch (option) {
        case "Make an Order":
            window.location.href = "index.html";
            // Implement logic to open Order Page
            break;
        case "Make Reservation":
            window.location.href = "makeRes.html";
            // Implement logic to open Make Reservation Page
            break;
        case "Check Reservation":
            // Implement logic to open Reservation Page
            break;
        case "Update Menu":
            // Implement logic to open Update Menu Page
            break;
        case "Order Stock":
            // Implement logic to open Order Stock Page
            break;
        case "Payment History":
            // Implement logic to open Payment History Page
            break;
        case "Edit Users":
            // Implement logic to open User Database Page
            break;
        case "Order Management":
            // Implement logic to open Order Management Page
            break;
        case "Exit":
            // Implement logic to exit the application
            break;
        default:
            // Create a new window for the selected option
            alert("This is the " + option + " page.");
            break;
    }
}
