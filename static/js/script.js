// Example JavaScript code to handle button clicks or other dynamic events
document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll("button");

    buttons.forEach(button => {
        button.addEventListener("click", () => {
            alert(`You clicked on ${button.innerText}`);
        });
    });
});
