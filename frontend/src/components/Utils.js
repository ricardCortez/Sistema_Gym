export const menuOptions = {
  admin: [
    { name: 'Gestión de Usuarios', url: '/gestion-usuarios' },
    { name: 'Reportes', url: '/reportes' },
    { name: 'Configuración', url: '/configuracion' },
    { name: 'Finanzas', url: '/finanzas' },
    { name: 'Promociones', url: '/promociones' },
    { name: 'Productos', url: '/productos' },
    { name: 'Perfil', url: 'perfil' }
  ],
  dueño: [
    { name: 'Reportes', url: '/reportes' },
    { name: 'Finanzas', url: '/finanzas' },
    { name: 'Promociones', url: '/promociones' },
    { name: 'Productos', url: '/productos' },
    { name: 'Perfil', url: '/perfil' }
  ],
  counter: [
    { name: 'Reportes', url: '/reportes' },
    { name: 'Promociones', url: '/promociones' },
    { name: 'Productos', url: '/productos' },
    { name: 'Perfil', url: '/perfil' }
  ]
};

export const getMenu = (userType) => {
  return menuOptions[userType] || [];
};
