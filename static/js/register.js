const formRegister = document.getElementById('form-register');

const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const passwordConfirmInput = document.getElementById('confirm-password');

const loginButton = document.getElementById('btn-login');


if (localStorage.getItem("token") !== null) {
    console.log(localStorage.getItem("token"));
    window.location.replace("/home");
}


formRegister.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("username", usernameInput.value);
    formData.append("password", passwordInput.value);

    if (passwordInput.value !== passwordConfirmInput.value) {
        alert("Your passwords doesn't match");
        return;
    }

    fetch("/register", {
        method: "POST",
        body: formData,
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("Data", data);

        if (data.result === "success") {
            window.location.replace("/login");
        } else {
            alert("Username already exists!");
        }
    })
    .catch((err) => {
        console.log("Error", err);
    })
})


$(loginButton).click(() => {
    window.location.replace("/login");
});
