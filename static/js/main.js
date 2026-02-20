console.log("Theme script loaded");
document.addEventListener("DOMContentLoaded", () => {
    const themeBtn = document.getElementById("theme-toggle");

    if (themeBtn) {
        themeBtn.addEventListener("click", () => {
            fetch("/toggle-theme/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
            .then(r => r.json())
            .then(data => {
                if (data.dark) {
                    document.body.classList.add("dark");
                    themeBtn.innerHTML = "☀️";
                } else {
                    document.body.classList.remove("dark");
                    themeBtn.innerHTML = "🌙";
                }
            });
        });
    }
});

function addToCart(gameId) {
    fetch(`/add-to-cart/${gameId}/`, {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
    .then(r => r.json())
    .then(data => {
        document.getElementById("cart-counter").innerText = data.cart_count;
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
