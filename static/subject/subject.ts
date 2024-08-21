document.addEventListener("DOMContentLoaded", function() {
    let button = document.getElementById("add-grade-button")!;
    button.addEventListener("click", function() {
        showSection(button);
    });

    let subject = window.location.href

    let formGrade = document.getElementById("add-grade-section")!;
    formGrade.addEventListener('submit', function(event) {
        event.preventDefault()

        let grade = (document.getElementById("grade") as HTMLTextAreaElement)!.value;
        let gradeWeight = (document.getElementById("grade-weight") as HTMLTextAreaElement)!.value;
        const regex = /^[a-zA-z]+$/;
        if (!!regex.test(grade) && !!regex.test(gradeWeight)) {
            window.alert("letters detected in the grade or in the grade weight")
            return false
        };

        const data = {
            subject: document.title,
            grade: grade,
            code: '002',
            date: (document.getElementById("grade-date") as HTMLTextAreaElement)!.value,
            grade_weight: gradeWeight,
            type: (document.getElementById('type') as HTMLSelectElement)!.value
        };

        fetch("http://127.0.0.1:5000/"+document.title, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message.startsWith('grade added')) {
                window.alert(data.message)
                window.location.reload()
            } else {
                window.alert(data.message)
            }
        })
        .catch(error => console.error('error: ', error));
    });
});

function showSection(button: HTMLElement) {
    document.getElementById("add-grade-section")!.style.display = 'flex';
    button.style.display = 'none';
};