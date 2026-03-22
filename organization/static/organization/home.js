// Credit to Gemini 3.1 Pro for suggesting using JS for scrolling message box down
// (and for showing me some of this logic, though I wrote this myself)
// adding this event listener is likely overkill, but it just ensures this won't fire until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", (_event) => {
    scrollMessagesToBottom();
});

// Credit to Google AI overview for suggesting using the keyup event listener to display an error message when message input is too long
// I wrote this myself, though
document.addEventListener("keyup", (event) => {
    resizeMessageTextAreaAndDisplayInputErrorMessage();
    scrollMessagesToBottom();
})

document.addEventListener("keydown", (event) => {
    resizeMessageTextAreaAndDisplayInputErrorMessage();
    scrollMessagesToBottom();
})

function resizeMessageTextAreaAndDisplayInputErrorMessage() {
    const messageTextBox = document.getElementById("messageTextBox");
    const inputErrorMessageElement = document.getElementById("inputErrorMessageElement");
    const messageSubmitButton = document.getElementById("messageSubmitButton");
    const messageComposerContainer = document.getElementById("messageComposerContainer");

    autoResizeTextArea(messageTextBox);
    displayInputErrorMessage(messageTextBox, inputErrorMessageElement, messageSubmitButton, messageComposerContainer);

    const messageContainer = document.getElementById("messageContainer");
    messageContainer.scrollBy(0, messageContainer.scrollHeight - messageContainer.clientHeight);
}

// learned how to make a text area auto-resizing from here:
// https://stackoverflow.com/questions/454202/creating-a-textarea-with-auto-resize
function autoResizeTextArea(textArea) {
    textArea.style.height = 'auto';
    if (textArea.scrollHeight < 200) textArea.style.height = textArea.scrollHeight + "px";
    else textArea.style.height = "200px";
}

function displayInputErrorMessage(messageTextBox, inputErrorMessageElement, messageSubmitButton, messageComposerContainer) {
    if (messageTextBox.value.length > 2000){
        inputErrorMessageElement.className = "text-danger";  // show error message
        messageSubmitButton.setAttribute("disabled", "true");  // disable send button
        // padding on bottom will be replaced with the error message (which has a height of 30px)
        messageComposerContainer.style.paddingBottom = "0";
    } else {
        inputErrorMessageElement.className = "text-danger d-none";  // hide error message
        if (messageSubmitButton.getAttribute("data-exec-only") !== "true" || messageSubmitButton.getAttribute("data-user-is-exec") === "true") {  // don't re-enable if page is exec only
            messageSubmitButton.removeAttribute("disabled");  // re-enable send button
        }
        messageComposerContainer.style.paddingBottom = "30px";  // replace padding on bottom
    }
}

// Reference for how this work:
// https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollBy
// https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight
// https://developer.mozilla.org/en-US/docs/Web/API/Element/clientHeight
function scrollMessagesToBottom() {
    const messageContainer = document.getElementById("messageContainer");
    messageContainer.scrollBy(0, messageContainer.scrollHeight - messageContainer.clientHeight);
}