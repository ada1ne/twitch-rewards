function handleSubmitActiveTrophies(e) {
    e.preventDefault();
    const checked_trophies = [...document.querySelectorAll('.active-trophy-option:checked')];
    const checked_trophies_ids = checked_trophies.map((trophy_element) => trophy_element.getAttribute("data-trophy-id"));

    alert(`Checked trophies are ${JSON.stringify(checked_trophies_ids)}`);
}

document.getElementById('submit-active-trophies').addEventListener("click", handleSubmitActiveTrophies);
