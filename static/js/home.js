const imgInput = $('#avatar');
const uploadBtn = $('#upload-btn');
const maskBtn = $('#mask-btn');
const generateBtn = $('#generate-btn');
const img = $("#image");

let filename = '';
let imgPath = '';
let maskName = '';


document.querySelector('#upload-btn').disabled = true;
document.querySelector('#mask-btn').disabled = true;
document.querySelector('#generate-btn').disabled = true;


imgInput.click(() => {
    document.querySelector('#upload-btn').disabled = false;
    document.querySelector('#mask-btn').disabled = true;
    document.querySelector('#generate-btn').disabled = true;
});

uploadBtn.click(() => {
    file = imgInput.prop('files')[0];
    let formData = new FormData();
    formData.append('file', file);

    $.ajax({
        url: 'http://127.0.0.1:8000/upload',
        data: formData,
        method: 'post',
        processData: false,
        contentType: false,
        success: (result) => {
            console.log(result);
            statusUpload = result.status
            if (statusUpload === 'grayscale') {
                alert("Изображение должно иметь три канала цветов")
            }
            else if (statusUpload === 'small') {
                alert("Изображение должно быть минимум 256 на 256")
            }
            else {
                img.attr("src", `/static/images/${result.filename}`);
                filename = result.filename;
                imgPath = result.path;

                document.querySelector('#mask-btn').disabled = false;
                document.querySelector('#generate-btn').disabled = true;
            }
        },
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
});


maskBtn.click(() => {
    $.ajax({
        url: 'http://127.0.0.1:8000/mask',
        data: JSON.stringify({'filename': filename, 'path': imgPath}),
        method: 'post',
        contentType: "application/json",
        dataType: 'json',
        success: (result) => {
            console.log(result);
            img.attr("src", `data:image/png;base64,${result.file}`);
            maskName = result.mask_name;

            document.querySelector('#generate-btn').disabled = false;
        },
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
});


generateBtn.click(() => {
    document.querySelector('#avatar').disabled = true;
    document.querySelector('#upload-btn').disabled = true;
    document.querySelector('#mask-btn').disabled = true;
    document.querySelector('#generate-btn').disabled = true;
    var i = 0;
    function move() {
        if (i == 0) {
            i = 1;
            var elem = document.getElementById("myBar");
            var width = 10;
            var id = setInterval(frame, 10);
            function frame() {
            if (width >= 100) {
                clearInterval(id);
                i = 0;
            } else {
                width++;
                elem.style.width = width + "%";
                elem.innerHTML = width + "%";
            }
            }
        }
    }
    move();

    $.ajax({
        url: 'http://127.0.0.1:8000/generate',
        data: JSON.stringify({'mask_name': maskName, 'path': imgPath}),
        method: 'post',
        contentType: "application/json",
        dataType: 'json',
        success: (result) => {
            console.log(result);
            img.attr("src", `data:image/png;base64,${result.file}`);

            document.querySelector('#avatar').disabled = false;
            document.querySelector('#upload-btn').disabled = false;
            document.querySelector('#mask-btn').disabled = false;
            document.querySelector('#generate-btn').disabled = false;
        },
        error: function(xhr, status, error) {
            console.log(xhr.responseText);
        }
    });
});