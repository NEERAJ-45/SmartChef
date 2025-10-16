function showAlert(message, type="success") {
    const alertBox = document.createElement("div");
    alertBox.className = `fixed top-5 right-5 px-4 py-2 rounded-lg shadow-lg text-white transition ${
        type === "success" ? "bg-green-500" : "bg-red-500"
    }`;
    alertBox.textContent = message;
    document.body.appendChild(alertBox);

    setTimeout(() => {
        alertBox.classList.add("opacity-0");
        setTimeout(() => alertBox.remove(), 500);
    }, 3000);
}

function handleCalories(event) {
    event.preventDefault();
    const input = event.target.recipe_input.value.trim();
    if (!input) {
        showAlert("Please enter recipe data!", "error");
        return false;
    }
    event.target.submit();
    showAlert("Calories calculated successfully!", "success");
}

function handleCompare(event) {
    event.preventDefault();
    const ing1 = event.target.ing1.value.trim();
    const ing2 = event.target.ing2.value.trim();
    if (!ing1 || !ing2) {
        showAlert("Please enter both ingredients!", "error");
        return false;
    }
    event.target.submit();
    showAlert("Comparison done!", "success");
}

function handleShopping(event) {
    event.preventDefault();
    const input = event.target.shopping_input.value.trim();
    if (!input) {
        showAlert("Please enter shopping list!", "error");
        return false;
    }
    event.target.submit();
    showAlert("Shopping list generated!", "success");
}

function handleSuggest(event) {
    event.preventDefault();
    const input = event.target.available.value.trim();
    if (!input) {
        showAlert("Please enter available ingredients!", "error");
        return false;
    }
    event.target.submit();
    showAlert("Recipe suggestions ready!", "success");
}
