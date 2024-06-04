Voy a actualizar el README.md con la información adicional sobre el uso de WhatsApp para enviar alertas de vencimiento de membresías y las tecnologías utilizadas en el front-end y back-end.

### README.md Actualizado

```markdown
# Sistema de Gestión Interna para Gimnasios

Este sistema permite automatizar el registro de socios nuevos y entrenadores, utilizando reconocimiento facial para marcar el ingreso y salida, gestionando contratos, membresías, gastos, y generando diversos reportes para una administración eficiente del gimnasio.

## Tabla de Contenidos
- [Descripción](#descripción)
- [Instalación](#instalación)
- [Uso](#uso)
- [Características](#características)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Descripción

El Sistema de Gestión Interna para Gimnasios permite:
- Automatizar el registro de socios y entrenadores.
- Utilizar reconocimiento facial para marcar el ingreso y salida de socios y entrenadores.
- Gestionar contratos, membresías y productos vendidos.
- Generar reportes de asistencia, gastos y ventas.
- Comunicar directamente con socios a través de WhatsApp.

## Instalación

Para instalar y configurar el proyecto localmente, sigue estos pasos:

```bash
git clone https://github.com/tu_usuario/sistema_gestion_gimnasios.git
cd sistema_gestion_gimnasios
pip install -r requirements.txt
```

## Uso

Para iniciar el sistema, usa el siguiente comando:

```bash
python app.py
```

Puedes acceder al sistema a través de `http://localhost:5000`.

## Características

### Gestión de Socios
- Registro y gestión de datos completos de socios.
- Asignación automática de un código único para cada socio.
- Gestión de membresías, pagos y renovaciones.
- Comunicación directa con socios a través de WhatsApp.

### Integración de Promociones de Membresías
- Integración de promociones especiales al asignar membresías.
- Cálculo automático de la duración de la membresía según la promoción seleccionada.

### Alertas por WhatsApp sobre Mantenimientos o Cierre
- Programación de alertas por WhatsApp sobre mantenimientos programados o cierre temporal del gimnasio.
- Envío automático de mensajes a todos los socios para informarles sobre la situación y cualquier cambio en los horarios de atención.

### Alertas de Vencimiento de Membresías
- Envío de alertas por WhatsApp a los socios próximos a vencer su membresía.
- Mensajes automáticos enviados unos días antes de la fecha de vencimiento para recordar a los socios la renovación de su membresía.

### Asignación de Entrenamientos Personalizados
- Asignación de entrenamientos personalizados a cada entrenador con plazos de inicio y fin.
- Renovación automática de entrenamientos al finalizar el plazo.

### Control de Acceso
- Verificación de ingreso de socios mediante código único asociado al reconocimiento facial.
- Registro de entrada y salida para control de asistencia.
- Verificación de ingreso de los entrenadores mediante el reconocimiento facial.

### Gestión de Pagos y Finanzas
- Procesamiento de pagos de membresías y servicios adicionales.
- Generación automática de facturas con plantilla editable.
- Registro de ingresos por días libres y membresías para el cálculo de las finanzas.
- Generación de informes de ingresos descargables en formato Excel.

### Venta de Productos de Gimnasio
- Registro y gestión de productos disponibles en el gimnasio.
- Asignación de precios y categorías a los productos.
- Control de stock y notificaciones de productos agotados.
- Registro de ventas de productos y generación de informes de ventas.

## Tecnologías Utilizadas

- **Lenguajes**: Python
- **Frameworks**: Flask (Back-end), React (Front-end)
- **Bibliotecas**: OpenCV, SQLAlchemy
- **Base de Datos**: PostgreSQL
- **Otros**: WhatsApp API, Excel

## Contribuir

Si deseas contribuir al proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la licencia MIT - mira el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

4mars - [@4mars](https://x.com/_4mars)

Enlace al Proyecto: [[https://github.com/ricardCortez/sistema_gestion_gimnasios](https://github.com/ricardCortez/Sistema_Gym)])
```

Este README.md actualizado incluye la información sobre el envío de alertas de vencimiento de membresías a través de WhatsApp y las tecnologías utilizadas en el front-end y back-end. Si necesitas más detalles o algún ajuste adicional, por favor házmelo saber.
