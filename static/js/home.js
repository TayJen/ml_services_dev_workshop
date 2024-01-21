const usernameBalanceLabel = document.getElementById('lbl-username-balance');
const logoutButton = document.getElementById('btn-logout');

const csvInput = document.getElementById('upload-data-csv');
const modelSelect = document.getElementById('model-select');
const predictButton = document.getElementById('btn-predict');

const historyBody = document.getElementById('table-user-history');


function checkTokenAndRedirect() {
    if (localStorage.getItem('token') === null) {
        window.location.replace("/login");
    }
}

function onStartup() {
    checkTokenAndRedirect();
    predictButton.disabled = true;

    fetch("/current_user", {
        method: "POST",
        body: localStorage.getItem('token'),
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("Data", data);

        if (data.result === "success") {
            $(usernameBalanceLabel).empty();
            usernameBalanceLabel.append(`User: ${data.username} Balance: ${data.balance}`);
            createTable(data.user_history);
        } else {
            localStorage.removeItem('token');
            window.location.replace("/login");
        }
    })
    .catch((err) => {
        console.log("Error", err);
    })
}

onStartup();


$(logoutButton).click(() => {
    localStorage.removeItem('token');
    checkTokenAndRedirect();
});


$(csvInput).change(() => {
    if (csvInput.files[0]) {
        predictButton.disabled = false;
    }
});


$(predictButton).click(() => {
    console.log(localStorage.getItem('token'));
    console.log(csvInput.files[0]);
    console.log(modelSelect.value);

    formData = new FormData();
    formData.append('token', localStorage.getItem('token'));
    formData.append('file', csvInput.files[0]);
    formData.append('model_choice', modelSelect.value);

    fetch("/predict", {
        method: "POST",
        body: formData
    })
    .then((res) => res.json())
    .then((data) => {
        console.log("Data", data);
        onStartup();
    })
    .catch((err) => {
        console.log("Error", err);
    })
});


function createTable(userHistory) {
    console.log(userHistory);

    $(historyBody).empty();

    userHistory.forEach(historyElement => {
        let dateCreated = historyElement.date;
        let modelName = historyElement.model_name;
        let predictionsTime = historyElement.predictions_time;
        let answers = historyElement.answers;

        let rowspan = predictionsTime.length + 1;
        let historyElementRows = `<tr><td rowspan=${rowspan}>${dateCreated}</td><td rowspan=${rowspan}>${modelName}</td></tr>`;
        for (let i = 0; i < predictionsTime.length; i++) {
            let predictionRow = `<tr><td>${predictionsTime[i]}</td><td>${answers[i]}</td></tr>`;
            historyElementRows = historyElementRows + predictionRow;
        }
        // <tr>
        //     <td rowspan=4>24.11.2023 15:48</td>
        //     <td rowspan=4>LogisticRegression</td>
        // </tr>
        // <tr>
        //     <td>0.78</td>
        //     <td>1</td>
        // </tr>
        $(historyBody).append($(historyElementRows));
    });
}
