$(document).ready(function() {
    $('form[name="formularioInicioSesion"]').on('submit', function(e) {
        // Evitar que el formulario se envíe de la forma tradicional
        e.preventDefault();

        // Obtener los valores del formulario
        var username = $('input[name="username"]').val();
        var password = $('input[name="password"]').val();

        // Verificar si los campos están vacíos
        if (username === "" || password === "") {
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Por favor, complete todos los campos.'
            });
            return;
        }

        // Enviar los datos a tu servidor para la autenticación
        $.ajax({
            type: "POST",
            url: "/",
            data: {
                'username': username,
                'password': password
            },
            dataType: 'text',  // Especifica que se espera una respuesta de tipo texto
            success: function(data) {
                // Si el inicio de sesión es exitoso, redirigir a la página de inicio
                if (data === 'Inicio de sesión exitoso') {
                    Swal.fire({
                        icon: 'success',
                        title: 'Inicio correcto',
                        timer: 1500,  // Tiempo en milisegundos que se mostrará el mensaje antes de redirigir
                        showConfirmButton: false
                    });
                    setTimeout(function() {
                        window.location.href = '/';  // Redirige a la página de inicio después del login exitoso
                    }, 1500);
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Inicio de sesión fallido',
                        text: data
                    });
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                // Si hay un error, mostrar un mensaje de error genérico
                Swal.fire({
                    icon: 'error',
                    title: 'Error en la solicitud',
                    text: 'Por favor, intenta nuevamente.'
                });
            }
        });
    });
});
