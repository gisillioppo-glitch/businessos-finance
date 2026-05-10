const form = document.querySelector("#demo-request-form");
const statusNode = document.querySelector("#form-status");

function isPlaceholderEndpoint(action) {
  return action.includes("REPLACE_WITH_FORM_ID") || action.trim() === "";
}

if (form) {
  form.addEventListener("submit", (event) => {
    const formData = new FormData(form);
    const honeypotValue = formData.get("website");

    if (honeypotValue) {
      event.preventDefault();
      return;
    }

    if (isPlaceholderEndpoint(form.action)) {
      event.preventDefault();
      statusNode.textContent = "Demo request captured locally for MVP review. Connect a form endpoint to send automatic emails.";
      statusNode.dataset.state = "pending";
      form.reset();
    }
  });
}
