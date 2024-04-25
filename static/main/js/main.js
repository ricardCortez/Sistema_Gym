$(document).ready(function() {
    // Cerrar sesión al hacer clic en el botón
    $('button[name="cerrarSesion"]').on('click', function(e) {
        e.preventDefault();

        // Enviar una solicitud al servidor para cerrar la sesión
        $.ajax({
            type: "POST",
            url: "/logout",  // URL para cerrar la sesión en el backend
            dataType: 'text',
            success: function(data) {
                // Redirigir a la página de inicio de sesión después de cerrar sesión
                window.location.href = '/';
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("Error al cerrar la sesión.");
            }
        });
    });
});
