let isLoginMode = true;

document.getElementById("auth-form").addEventListener("submit", (e) => {
    e.preventDefault();

    if (isLoginMode) {
        // 🔐 LOGIN
        const username = document.getElementById("login-username").value;
        const password = document.getElementById("login-password").value;

        const users = JSON.parse(localStorage.getItem("users")) || [];

        const user = users.find(u => u.username === username && u.password === password);

        if (user) {
            alert("✅ Login successful");
        } else {
            alert("❌ Invalid credentials");
        }

    } else {
        // 📝 REGISTER
        const username = document.getElementById("reg-username").value;
        const email = document.getElementById("reg-email").value;
        const password = document.getElementById("reg-password").value;
        const confirm = document.getElementById("reg-confirm").value;

        if (password !== confirm) {
            alert("❌ Passwords do not match");
            return;
        }

        let users = JSON.parse(localStorage.getItem("users")) || [];

        const exists = users.find(u => u.username === username);

        if (exists) {
            alert("⚠️ Username already exists");
            return;
        }

        users.push({ username, email, password });
        localStorage.setItem("users", JSON.stringify(users));

        alert("✅ Registration successful");

        showLogin(); // cleaner switch
/* 🔁 Toggle */
toRegisterLink.addEventListener("click", () => {
    loginFields.style.display = "none";
    registerFields.style.display = "block";
    card.classList.add("register");
});

toLoginLink.addEventListener("click", () => {
    loginFields.style.display = "block";
    registerFields.style.display = "none";
    card.classList.remove("register");
});

    }
});