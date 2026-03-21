// Credit to Gemini 3.1 Pro for suggesting using JS for this (and for showing me some of this logic, though I wrote this myself)

// adding this event listener is likely overkill, but it just ensures this won't fire until the DOM is fully loaded
addEventListener("DOMContentLoaded", (_event) => {
    const messageContainer = document.getElementById("messageContainer");

    // Reference for how this work:
    // https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollBy
    // https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight
    // https://developer.mozilla.org/en-US/docs/Web/API/Element/clientHeight
    messageContainer.scrollBy(0, messageContainer.scrollHeight - messageContainer.clientHeight);
});