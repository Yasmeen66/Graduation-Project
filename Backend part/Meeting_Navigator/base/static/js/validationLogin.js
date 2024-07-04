document.getElementById("loginForm").addEventListener("submit", function(event) {
    let isValid = true;

    // Email validation
    const email = document.getElementById("email");
    const emailError = document.getElementById("emailError");
    const emailPattern = /^[^\s@]+@[^\s@]+\.(com|edu|org)$/;
    if (!emailPattern.test(email.value)) {
        email.classList.add("invalid");
        emailError.textContent = "Invalid email address. Only .com, .edu, or .org domains are allowed.";
        isValid = false;
    } else {
        email.classList.remove("invalid");
        emailError.textContent = "";
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

    // If the form is not valid, prevent submission
    if (!isValid) {
        event.preventDefault(); // Prevent form submission
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
