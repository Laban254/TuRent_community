// JavaScript code
document.addEventListener("DOMContentLoaded", function() {
  const editButton = document.getElementById("edit_button");
  const saveButton = document.getElementById("save_button");
  const form = document.getElementById("edit_form");
  const textFields = document.querySelectorAll(".text_box");

  // Enable editing when the Edit Information button is clicked
  editButton.addEventListener("click", function() {
      for (const field of textFields) {
          field.removeAttribute("disabled");
      }
      editButton.style["display"]="none";
  });

  
});
