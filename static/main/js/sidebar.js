document.addEventListener("DOMContentLoaded", function() {
  // Obtener todos los elementos con la clase "dropdown"
  var dropdowns = document.querySelectorAll(".dropdown");

  // Agregar un evento de clic a cada elemento "dropdown"
  dropdowns.forEach(function(dropdown) {
    dropdown.addEventListener("click", function(event) {
      // Evitar el comportamiento predeterminado del enlace
      event.preventDefault();

      // Mostrar u ocultar el menú desplegable correspondiente
      var dropdownContent = dropdown.querySelector(".dropdown-content");
      dropdownContent.style.display = dropdownContent.style.display === "block" ? "none" : "block";
    });
  });

  // Cerrar el menú desplegable al hacer clic fuera de él
  document.addEventListener("click", function(event) {
    if (!event.target.closest(".dropdown")) {
      dropdowns.forEach(function(dropdown) {
        var dropdownContent = dropdown.querySelector(".dropdown-content");
        dropdownContent.style.display = "none";
      });
    }
  });
});
