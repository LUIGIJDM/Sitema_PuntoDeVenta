
# Sistema de Punto de Venta (POS) con Tkinter y MySQL
Este proyecto es un sistema de punto de venta (POS) simple desarrollado en Python utilizando la biblioteca Tkinter para la interfaz gráfica y MySQL para el almacenamiento de datos. Permite a los administradores agregar, buscar, eliminar y ver el inventario de productos, mientras que los clientes pueden navegar por los productos, agregarlos a un carrito de compras y finalizar la compra.

## Características
### Inicio de sesión: 
 - El sistema cuenta con un inicio de sesión para diferenciar entre administradores y clientes.
### Panel de administración:
 - Agregar nuevos productos con nombre, serie, cantidad y precio.
 - Buscar productos por nombre.
 - Eliminar productos.
 - Editar productos.
 - Visualizar el inventario completo en una tabla.
### Panel del cliente:
 - Muestra la lista de productos disponibles con su información (nombre, serie, cantidad en stock y precio).
 - Permite al cliente seleccionar la cantidad deseada de cada producto.
 - Valida el stock disponible antes de agregar al carrito.
 - Muestra un carrito de compras con los productos seleccionados y el total.
 - Permite finalizar la compra, confirmando o cancelando.
### Actualización del inventario: 
 - El stock de productos se actualiza automáticamente en la base de datos al finalizar una compra.

## Requisitos
 - Python: Asegúrate de tener Python instalado en tu sistema. Puedes descargarlo desde https://www.python.org/.
 - Tkinter: Esta biblioteca suele venir incluida con Python. Si no la tienes, puedes instalarla con pip install tkinter.
 - MySQL Connector: Instala el conector de MySQL para Python con pip install mysql-connector-python.
 - XAMPP: Necesitas XAMPP (o un servidor MySQL similar) para ejecutar la base de datos. Descárgalo desde https://www.apachefriends.org/.
 - Pillow (PIL): Para cargar y mostrar imágenes, instala Pillow con pip install Pillow.

## Configuración
### Base de datos:
 - Crea una base de datos MySQL llamada "tienda".
 - Crea una tabla llamada "productos" con las columnas:
   * nombre (VARCHAR)
   * serie (VARCHAR)
   * cantidad (VARCHAR)
   * precio (FLOAT)

### Credenciales:
 - Reemplaza "localhost", "root" y "" (contraseña) en el código con tus credenciales de MySQL.

### Logo:
 - Reemplaza "logoft.png" con la ruta de tu archivo de logo o elimina esa parte del código si no necesitas un logo.

## Uso
 - Ejecutar: Guarda el código como un archivo Python (por ejemplo, pos.py) y ejecútalo desde tu terminal con python pos.py.

- Iniciar sesión:
   - Para acceder como administrador, usa el usuario "admin" y la contraseña "admin".
   - Para acceder como cliente, usa el usuario "cliente" y la contraseña "cliente". (Nota: Estas credenciales son solo de ejemplo y deberías cambiarlas en un entorno real).

 - Panel de administración:
   - Utiliza los botones para agregar, buscar, eliminar y ver el inventario.
 - Panel del cliente:
   - Selecciona los productos y cantidades que deseas comprar.
   - Haz clic en "Finalizar compra" para ver el resumen y confirmar o cancelar.

## Consideraciones adicionales
 - Seguridad: En una aplicación real, es crucial implementar medidas de seguridad más robustas para proteger la base de datos y las credenciales de acceso.
 - Funcionalidades: Este es un sistema básico. Podrías agregar más características como:
   - Gestión de usuarios.
   - Generación de facturas o recibos.
   - Integración con sistemas de pago.
   - Opciones de búsqueda y filtrado más avanzadas.
 - Diseño: La interfaz gráfica es muy simple. Podrías mejorarla con un diseño más atractivo y fácil de usar.

## Licencia
Este proyecto se distribuye bajo la Licencia MIT.

*¡Siéntete libre de contribuir y mejorar este proyecto!*

