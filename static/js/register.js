const usernameInput = $('#username');
const passwordInput = $('#password');
const passwordConfirmInput = $('#confirm-password');
const submitButton = $('#submit');

// const formRegister = $('#form-register');

const formRegister = document.querySelector("#form-register")


formRegister.addEventListener("submit", (e) => {
    e.preventDefault();
    const formData = new FormData(formRegister);
    console.log(formData);

    fetch("https://localhost:8000/register", {
        method: "POST",
        body: formData,
    })
    .then((res) => res.json())
    .then((token) => {
        console.log("Token", token);
        // window.location.href = "/"
    })
    .catch((err) => {
        console.log("Error", err);
    })
})






// submitButton.click(() => {
//     file = imgInput.prop('files')[0];
//     let formData = new FormData();
//     formData.append('file', file);

//     $.ajax({
//         url: 'http://127.0.0.1:8000/upload',
//         data: formData,
//         method: 'post',
//         processData: false,
//         contentType: false,
//         success: (result) => {
//             console.log(result);
//             statusUpload = result.status
//             if (statusUpload === 'grayscale') {
//                 alert("Изображение должно иметь три канала цветов")
//             }
//             else if (statusUpload === 'small') {
//                 alert("Изображение должно быть минимум 256 на 256")
//             }
//             else {
//                 img.attr("src", `/static/images/${result.filename}`);
//                 filename = result.filename;
//                 imgPath = result.path;

//                 document.querySelector('#mask-btn').disabled = false;
//                 document.querySelector('#generate-btn').disabled = true;
//             }
//         },
//         error: function(xhr, status, error) {
//             console.log(xhr.responseText);
//         }
//     });
// });
