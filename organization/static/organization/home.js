// Credit to Gemini 3.1 Pro for suggesting using JS for scrolling message box down
// (and for showing me some of this logic, though I wrote this myself)
// adding this event listener is likely overkill, but it just ensures this won't fire until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", (_event) => {
    const messageContainer = document.getElementById("messageContainer");

    // Reference for how this work:
    // https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollBy
    // https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight
    // https://developer.mozilla.org/en-US/docs/Web/API/Element/clientHeight
    messageContainer.scrollBy(0, messageContainer.scrollHeight - messageContainer.clientHeight);
});

// Credit to Google AI overview for suggesting using the keyup event listener to display an error message when message input is too long
// I wrote this myself, though
document.addEventListener("keyup", (event) => {
    displayInputErrorMessage();
})

document.addEventListener("keydown", (event) => {
    displayInputErrorMessage();
})

function displayInputErrorMessage() {
    const messageTextBox = document.getElementById("messageTextBox");
    const messageInputError = document.getElementById("messageInputError");
    const messageSubmitButton = document.getElementById("messageSubmitButton");
    const messageComposerContainer = document.getElementById("messageComposerContainer");

    // learned how to make this auto-resizing from here:
    // https://stackoverflow.com/questions/454202/creating-a-textarea-with-auto-resize
    messageTextBox.style.height = 'auto';
    if (messageTextBox.scrollHeight < 200) messageTextBox.style.height = messageTextBox.scrollHeight + "px";
    else messageTextBox.style.height = "200px";

    if (messageTextBox.value.length > 2000){
        messageInputError.className = "text-danger mb-0";  // show error message
        messageSubmitButton.setAttribute("disabled", "true");  // disable send button
        messageComposerContainer.className = "px-3 px-md-4 border-top bg-body flex-shrink-0 pt-4";  // remove bottom padding to prevent visual shift
    } else {
        messageInputError.className = "text-danger mb-0 d-none";
        messageSubmitButton.removeAttribute("disabled");
        messageComposerContainer.className = "px-3 px-md-4 border-top bg-body flex-shrink-0 pt-4 pb-4";
    }
}