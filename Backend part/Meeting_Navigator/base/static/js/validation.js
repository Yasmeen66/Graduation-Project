document.getElementById("signupForm").addEventListener("submit", function(event) {
    event.preventDefault();
    let isValid = true;

    // Full name validation
    const name = document.getElementById("name");
    const nameError = document.getElementById("nameError");
    if (name.value.trim() === "") {
        name.classList.add("invalid");
        nameError.textContent = "Name is required.";
        isValid = false;
    } else {
        name.classList.remove("invalid");
        nameError.textContent = "";
    }

    // Email validation
    const email = document.getElementById("email");
    const emailError = document.getElementById("emailError");
    const emailPattern = /^[^\s@]+@[^\s@]+\.(com|edu|org|gov|net)$/;
    if (!emailPattern.test(email.value)) {
        email.classList.add("invalid");
        emailError.textContent = "Invalid email address. Only .com, .edu, .gov, .net or .org domains are allowed.";
        isValid = false;
    } else {
        email.classList.remove("invalid");
        emailError.textContent = "";
    }

    // Phone validation
    const phone = document.getElementById("phone");
    const phoneError = document.getElementById("phoneError");
    const phonePattern = /^\d{11}$/;
    if (!phonePattern.test(phone.value)) {
        phone.classList.add("invalid");
        phoneError.textContent = "Phone number must be 11 digits.";
        isValid = false;
    } else {
        phone.classList.remove("invalid");
        phoneError.textContent = "";
    }

    // Password validation
    const password = document.getElementById("password");
    const passwordError = document.getElementById("passwordError");
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
    if (!passwordPattern.test(password.value)) {
        password.classList.add("invalid");
        passwordError.textContent = "Password must be at least 8 characters long and contain digits, lowercase and uppercase letters.";
        isValid = false;
    } else {
        password.classList.remove("invalid");
        passwordError.textContent = "";
    }

    // If the form is valid, redirect to login.html
    if (isValid) {
        window.location.href = "login.html";
    }
});

// Show/Hide Password
document.getElementById("showPassword").addEventListener("change", function() {
    const password = document.getElementById("password");
    if (this.checked) {
        password.type = "text";
    } else {
        password.type = "password";
    }
});
