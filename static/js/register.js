const formRegister = document.getElementById('form-register');

const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const passwordConfirmInput = document.getElementById('confirm-password');


if (localStorage.getItem("token") !== null) {
    console.log(localStorage.getItem("token"));
    window.location.replace("http://localhost:8000/home");
}


formRegister.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("username", usernameInput.value);
    formData.append("password", passwordInput.value);

    console.log(formData);
    console.log(formData.get("username"));

    if (passwordInput.value !== passwordConfirmInput.value) {
        alert("Your passwords doesn't match");
        return;
    }

    fetch("http://localhost:8000/register", {
        method: "POST",
        body: formData,
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("Data", data);

        if (data.result === "success") {
            console.log(data.result);
            window.location.replace("http://localhost:8000/login");
        } else {
            alert("Username already exists!");
        }
    })
    .catch((err) => {
        console.log("Error", err);
    })
})

