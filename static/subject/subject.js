document.addEventListener("DOMContentLoaded", function () {
    var button = document.getElementById("add-grade-button");
    button.addEventListener("click", function () {
        showSection(button);
    });
    var subject = window.location.href;
    var formGrade = document.getElementById("add-grade-section");
    formGrade.addEventListener('submit', function (event) {
        event.preventDefault();
        var grade = document.getElementById("grade").value;
        var gradeWeight = document.getElementById("grade-weight").value;
        var regex = /^[a-zA-z]+$/;
        if (!!regex.test(grade) && !!regex.test(gradeWeight)) {
            window.alert("letters detected in the grade or in the grade weight");
            return false;
        }
        ;
        var data = {
            subject: document.title,
            grade: grade,
            code: '002',
            date: document.getElementById("grade-date").value,
            grade_weight: gradeWeight,
            type: document.getElementById('type').value
        };
        fetch("http://127.0.0.1:5000/" + document.title, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
            .then(function (response) { return response.json(); })
            .then(function (data) {
            if (data.message.startsWith('grade added')) {
                window.alert(data.message);
                window.location.reload();
            }
            else {
                window.alert(data.message);
            }
        })
            .catch(function (error) { return console.error('error: ', error); });
    });
});
function showSection(button) {
    document.getElementById("add-grade-section").style.display = 'flex';
    button.style.display = 'none';
}
;

function deleteGrade(id) {
    var data = {
        code: '004',
        id: id
    };
    fetch("http://127.0.0.1:5000/" + document.title, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(function (response) { return response.json(); })
    .then(function (data) {
    if (data.message.startsWith('grade deleted')) {
        window.alert(data.message);
        window.location.reload();
    }
    else {
        window.alert(data.message);
    }
    })
    .catch(function (error) { return console.error('error: ', error); });
}