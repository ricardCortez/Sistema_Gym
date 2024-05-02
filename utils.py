# utils.py

class menu_manager:
    menu_options = {
        'admin': [
            {'name': 'Gestión de Usuarios', 'url': '/gestion-usuarios'},
            {'name': 'Reportes', 'url': '/reportes'},
            {'name': 'Configuración', 'url': '/configuracion'},
            {'name': 'Finanzas', 'url': '/finanzas'},
            {'name': 'Promociones', 'url': '/promociones'},
            {'name': 'Productos', 'url': '/productos'},
            {'name': 'Perfil', 'url': '/perfil'}
        ],
        'dueño': [
            {'name': 'Reportes', 'url': '/reportes'},
            {'name': 'Finanzas', 'url': '/finanzas'},
            {'name': 'Promociones', 'url': '/promociones'},
            {'name': 'Productos', 'url': '/productos'},
            {'name': 'Perfil', 'url': '/perfil'}
        ],
        'counter': [
            {'name': 'Reportes', 'url': '/reportes'},
            {'name': 'Promociones', 'url': '/promociones'},
            {'name': 'Productos', 'url': '/productos'},
            {'name': 'Perfil', 'url': '/perfil'}
        ]
    }

    @staticmethod
    def get_menu(user_type):
        # Devuelve una lista vacía si el tipo no está definido
        return menu_manager.menu_options.get(user_type, [])