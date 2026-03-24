// Credit to Gemini 3.1 Pro for suggesting using JS for scrolling message box down
// (and for showing me some of this logic, though I wrote this myself)
// adding this event listener is likely overkill, but it just ensures this won't fire until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", (_event) => {
    scrollMessagesToBottom();
    addDeleteMessageButtonOnClicks();
    addMessageComposerEventListener();
});

// Claude Opus 4.6 suggested this pattern for passing the message id into the modal for deletion
// Related docs: https://getbootstrap.com/docs/5.3/components/modal/#events
function addDeleteMessageButtonOnClicks() {
    const deleteMessageModal = document.getElementById("deleteMessageModal");
    deleteMessageModal.addEventListener("show.bs.modal", (event) => {
        const messageId = event.relatedTarget.dataset.messageId;
        const deleteMessageInput = document.getElementById("deleteMessageInput");
        deleteMessageInput.setAttribute("value", messageId);
    });
}

function addMessageComposerEventListener() {
    const messageTextBox = document.getElementById("messageTextBox");
    // Credit to Google AI overview for suggesting using an event listener to display an error message when message input is too long
    // I wrote this myself, though
    // Credit to Claude Opus 4.6 for suggesting unifying my keyup and keydown event listeners as an input event listener
    messageTextBox.addEventListener("input", (event) => {
        const messageContainer = document.getElementById("messageContainer");
        const messageContainerHeightBeforeScroll = messageContainer.clientHeight;
        resizeMessageTextAreaAndDisplayInputErrorMessage();
        const messageContainerHeightAfterScroll = messageContainer.clientHeight;
        scrollMessagesBy(0, messageContainerHeightBeforeScroll - messageContainerHeightAfterScroll);
    });
}

function resizeMessageTextAreaAndDisplayInputErrorMessage() {
    const messageTextBox = document.getElementById("messageTextBox");
    const inputErrorMessageElement = document.getElementById("inputErrorMessageElement");
    const messageSubmitButton = document.getElementById("messageSubmitButton");
    const messageComposerContainer = document.getElementById("messageComposerContainer");

    autoResizeTextArea(messageTextBox);
    displayInputErrorMessage(messageTextBox, inputErrorMessageElement, messageSubmitButton, messageComposerContainer);
}

// learned how to make a text area auto-resizing from here:
// https://stackoverflow.com/questions/454202/creating-a-textarea-with-auto-resize
function autoResizeTextArea(textArea) {
    textArea.style.height = 'auto';
    if (textArea.scrollHeight < 200) textArea.style.height = textArea.scrollHeight + "px";
    else textArea.style.height = "200px";
}

function displayInputErrorMessage(messageTextBox, inputErrorMessageElement, messageSubmitButton, messageComposerContainer) {
    const messageLength = getTextAreaInputLengthDoubleCountingNewlines(messageTextBox);

    if (messageLength > 2000){
        inputErrorMessageElement.className = "text-danger";  // show error message
        messageSubmitButton.setAttribute("disabled", "true");  // disable send button
        // padding on bottom will be replaced with the error message (which has a height of 30px)
        messageComposerContainer.style.paddingBottom = "0";
    } else {
        inputErrorMessageElement.className = "text-danger d-none";  // hide error message
        if (
            messageSubmitButton.getAttribute("data-exec-only") !== "true" ||
            messageSubmitButton.getAttribute("data-user-is-exec") === "true"
        ) {  // don't re-enable if page is exec only and user is not exec
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

function scrollMessagesBy(x, y) {
    const messageContainer = document.getElementById("messageContainer");
    messageContainer.scrollBy(x, y);
}

// newlines are double counted since they are sent as 2 chars to the backend
function getTextAreaInputLengthDoubleCountingNewlines(textArea) {
    let textAreaLength = 0;
    for (let c of textArea.value) {
        if (c === "\n") textAreaLength += 2;
        else textAreaLength += 1;
    }
    return textAreaLength;
}