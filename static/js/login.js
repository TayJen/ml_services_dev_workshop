const formLogin = document.getElementById('form-login');

const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');

const registerButton = document.getElementById('btn-register');




if (localStorage.getItem("token") != null) {
    console.log(localStorage.getItem("token"));
    window.location.replace("http://localhost:8000/home");
}


formLogin.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("username", usernameInput.value);
    formData.append("password", passwordInput.value);

    fetch("http://localhost:8000/login", {
        method: "POST",
        body: formData,
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("Data", data);

        if (data.result === "success") {
            localStorage.setItem("token", data.access_token);
            window.location.replace("http://localhost:8000/home");
        } else {
            alert("Incorrect username or password!");
        }
    })
    .catch((err) => {
        console.log("Error", err);
    })
})


$(registerButton).click(() => {
    window.location.replace("http://localhost:8000/register");
});
