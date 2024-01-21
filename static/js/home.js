const usernameBalanceLabel = document.getElementById('lbl-username-balance');
const logoutButton = document.getElementById('btn-logout');


function onStartup() {
    const TOKEN = localStorage.getItem('token');

    if (TOKEN === null) {
        window.location.replace("http://localhost:8000/login");
    }

    fetch("http://localhost:8000/current_user", {
        method: "POST",
        body: TOKEN,
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("Data", data);

        if (data.result === "success") {
            $(usernameBalanceLabel).empty();
            usernameBalanceLabel.append(`User: ${data.username} Balance: ${data.balance}`);
        } else {
            alert("Something went wrong!");
        }
    })
    .catch((err) => {
        console.log("Error", err);
    })
}

onStartup();


$(logoutButton).click(() => {
    localStorage.removeItem('token');
    onStartup();
});

