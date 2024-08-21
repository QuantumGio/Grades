document.addEventListener("DOMContentLoaded", function() {
    let button = document.getElementById("add-subject-button")!;
    button.addEventListener("click", function() {
        showSection(button);
    });

    let formSubject = document.getElementById("add-subject-section")!;
    formSubject.addEventListener('submit', function(event) {
        event.preventDefault()

        let subject = (document.getElementById("subject") as HTMLTextAreaElement)!.value;
        const regex = /^[a-zA-z]+$/;
        if (!regex.test(subject)) {
            window.alert("special characters or numbers in subject name")
            return false
        };

        const data = {
            subject: subject,
            code: '001'
        };

        fetch("http://127.0.0.1:5000", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.message.startsWith('subject added')) {
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
    document.getElementById("add-subject-section")!.style.display = 'flex';
    button.style.display = 'none';
};

function redirect(subject: string) {

    const data = {
        subject_redirect: subject
    }

    fetch("https://cautious-bassoon-x6wvjvjjv9xf9q44-5000.app.github.dev/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            window.location.href = data.redirect;
        } else {
            window.alert("error while going to subject: "+subject)
        }
    })
    .catch(error => console.error('error: ', error));
}