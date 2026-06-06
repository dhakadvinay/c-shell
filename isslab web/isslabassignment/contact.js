const form = document.getElementById('contact-form');
const formContainer = document.getElementById('form-container');
const successMessage = document.getElementById('success-message');

form.addEventListener('submit', (event) => {
    event.preventDefault();

    let formIsValid = true;

    // Validate Name
    const nameInput = document.getElementById('name');
    const nameError = document.getElementById('name-error');
    if (nameInput.value.trim() === '') {
        nameError.innerText = "Name is required.";
        formIsValid = false;
    } else {
        nameError.innerText = "";
    }

    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('email-error');
    if (emailInput.value.includes('@') === false) {
        emailError.innerText = "Please enter a valid email containing '@'.";
        formIsValid = false;
    } else {
        emailError.innerText = "";
    }

    const msgInput = document.getElementById('message');
    const msgError = document.getElementById('message-error');
    if (msgInput.value.trim() === '') {
        msgError.innerText = "Message cannot be empty.";
        formIsValid = false;
    } else {
        msgError.innerText = "";
    }
    if (formIsValid === true) {
        formContainer.style.display = 'none';
        successMessage.style.display = 'block';
    }
});