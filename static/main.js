document.getElementById("chat-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const message = document.getElementById("user-input").value.trim();
    const language = document.getElementById("language-selector").value; // Get the selected language
    displayMessage("You", message);

    // Show loading animation
    const loading = document.getElementById("loading");
    loading.style.display = "block";

    // Call the GPT API
    const response = await callGptApi(message, language); // Pass the language parameter
    if (response) {
        // Display the response message
        displayMessage("She Rakshak AI", response);
    } else {
        // Display an error message
        displayMessage("She Rakshak AI", "Sorry, there was an error processing your message. Please try again later.");
    }

    // Hide loading animation
    loading.style.display = "none";

    // Reset the chat input
    document.getElementById("user-input").value = "";
});

// Add placeholder text for chat input
const userInput = document.getElementById("user-input");
userInput.placeholder = "Please describe your problem in detail";

function displayMessage(sender, message) {
    const chat = document.getElementById("chat");
    const messageDiv = document.createElement("div");
    messageDiv.innerHTML = `<b>${sender}:</b> ${message}`;
    chat.appendChild(messageDiv);
    chat.scrollTop = chat.scrollHeight; // Auto-scroll to the bottom of the chat
}

async function callGptApi(message, language) {
    try {
        const response = await fetch("/gpt", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `message=${encodeURIComponent(message)}&language=${encodeURIComponent(language)}`,
        });
        const data = await response.json();

        return data.response;
    } catch (error) {
        console.error("Error fetching GPT response:", error);
        return null;
    }
}
