function updateSelectedOption(pronouns_id) {
    let selector = document.querySelector(`#pronouns-selector [value="${pronouns_id}"]`);
    if (!selector) {
        selector = document.querySelector('#pronouns-selector [value="2"]');
    }
    selector.checked = true;
}

fetch("/users")
    .then((response) => {
        if (!response.ok) {
            alert('Algo deu errado. Avisa no Discord!');
        }
        else {
            response.json().then((r) => updateSelectedOption(r.pronouns_id));
        }
    });