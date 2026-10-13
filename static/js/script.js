console.log("script.js підключено");

// ---------- Пошук нотаток за заголовком ----------
const searchInput = document.querySelector("#search");
const noResults = document.querySelector("#no-results");

if (searchInput && noResults) {
    const cards = document.querySelectorAll(".note-card");

    searchInput.addEventListener("input", function () {
        const text = searchInput.value.toLowerCase();
        let visibleCount = 0;

        cards.forEach(function (card) {
            const title = card.dataset.title.toLowerCase();
            if (title.includes(text)) {
                card.classList.remove("hidden");
                visibleCount++;
            } else {
                card.classList.add("hidden");
            }
        });

        if (visibleCount === 0) {
            noResults.classList.remove("hidden");
        } else {
            noResults.classList.add("hidden");
        }
    });
}

// ---------- Підтвердження видалення ----------
const deleteForms = document.querySelectorAll(".delete-form");

deleteForms.forEach(function (form) {
    form.addEventListener("submit", function (event) {
        if (!confirm("Видалити цю нотатку?")) {
            event.preventDefault();
        }
    });
});
