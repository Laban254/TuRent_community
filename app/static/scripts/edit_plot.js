// JavaScript code
document.addEventListener("DOMContentLoaded", function() {
  const editButton = document.getElementById("edit_button");
  const saveButton = document.getElementById("save_button");
  const form = document.getElementById("edit_form");
  const textFields = form.querySelectorAll("input[type='text']");

  // Enable editing when the Edit Information button is clicked
  editButton.addEventListener("click", function() {
      for (const field of textFields) {
          field.removeAttribute("disabled");
      }
      saveButton.removeAttribute("disabled");
  });

  // Disable editing and submit the form when the Save button is clicked
  saveButton.addEventListener("click", function() {
      for (const field of textFields) {
          field.setAttribute("disabled", true);
      }
      saveButton.setAttribute("disabled", true);
      form.submit();
  });
});
