# Proyecto 1 - Parte Web (U - Games)
**Integrantes**
- Andrés Lostaunau
- Sebastián Calle
- Esteban Vásquez
## Descripción
El proyecto que hemos realizado simula una página web de una empresa de venta de videojuegos, en la cual un cliente podrá realizar compras de manera sencilla, teniendo así acceso al catálogo de los juego disponibles de la tienda y los precios de cada uno de los juegos. Además el cliente será capaz de crear una cuenta para la página web, donde se registrará, y tiene acceso a un inventario individual, en el que se almacenarán los videojuegos que decida comprar. Nuestra página web también simula transacciones de compra y de adición de fondos para el usuario.
## Objetivos
- Los clientes pueden registrarse por medio de un usuario y contraseña.
- Los clientes pueden acceder a su cuenta y logearse.
- Asímismo los clientes son capaces de cerrar sesión de su cuenta.
- Las personas que visitan la página web tienen acceso al catálogo de juegos de la tienda.
- Los clientes registrados pueden agregar cualquiera de los videojuegos a su inventario.
- Podrán eliminar cualquiera de los juegos agregardos a su inventario en caso de no querer realizar la compra.
- Al realizar una compra la transacción debe ser integra, de modo que no pueden haber ningún tipo de anomalías en la compra.
## Misión
La misión de nuestra página web es que las personas tengan un acceso más rápido y óptimo al momento de realizar las compras de videojuegos, en este caso simulando que somos una tienda de juegos que desea ofrecer sus productos. 
## Visión
La visión de nuestro proyecto es poder ofrecer a los usuarios la capacidad de revisar un amplio catálogo de videojuegos en las diferentes tiendas existentes, para que así pueda realizar sus compras o comparar los productos desde la comodidad de su casa y sin requerir mucho esfuerzo. 
##  Tecnologías usadas
### Base de datos
- PostgreSQL: Todo las tablas y los datos de la aplicación se almacenan en un base de datos de postgreSQL.
### Back-end
- Flask: Todo el back-end de la aplicación se ha creado utilizando Python-Flask para poder administrar las peticiones al servidor por parte del cliente.
- - Flask-SQLAlchemy: Es el ORM para poder crear una comunicación entre el back-end y la base de datos.
### Front-end
- HTML-JS-CSS:  El front-end fue diseñado en su plenitud usando estos tres componentes sin necesidad de un framework complementario.
- JQuery: Se empleó para facilitar el envío de mensajes por parte del front-end hacia el back-end con mensajes en formato JSON.
## Inicialización
El ORM (Flask-SQLAlchemy) crea las tablas en la base de datos si es que no existen. Para ejecutar por primera vez se tiene un script llamado _sqlscript.txt_ donde se encuentran los primeros inserts para la tabla juegos. Para reiniciar la base de datos se deben dar drop a todas las tablas, ejecutar la aplicación y volver a insertar los valores iniciales.
## Requests Info
### '/' & '/home' [GET]
Redirecciona a la página principal.
### '/register' [GET, POST]
GET: Recibe la página con el form para realizar el registro de un usuario nuevo.
POST: Recibe la información del form y lo valida. De ser válido lo agrega en la tabla de usuarios de la base de datos, y si no es válido regresa un flash con el error a '/register'.
### '/login' [GET, POST]
GET: Recibe la página con el form para realizar el login de un usuario.
POST: Recibe la información del form y lo valida. De ser válido lo busca en la tabla usuarios de la base de datos y guarda en el localStorage del front-end, y si no es válido regresa un flash con el error a '/login'.
### '/games' [GET, POST]
GET: Muestra el catálogo de juegos a disposición del usuario con su respectivo precio. Al darle click a un precio enviará una acción POST.
POST: Envía la compra al servidor en formato JSON y procesa su validación. Si es válida se creara una relación en la tabla de Inventario en la base de datos.
### '/profile/\<username>' [GET, POST]
GET: Muestra los datos del usuario.
POST: Realiza la operación de agregar fondos a la cuenta del usuario.
### '/inventory/\<username>' [GET, DELETE]
GET: Muestra una lista de los juegos en el inventario del usuario. Al darle click al botón de borrar enviará una acción DELETE.
DELETE: Manda una petición de borrado del juego en formato JSON.
## Hosts
Todas las operaciones se están realizando en _localhost:8080_ por el momento.
## Forma de autenticación
Para el login el usuario es autenticado buscando la información en la base de datos. El nombre de usuario es un atributo _unique_ por ende solo puede existir un usuario con el nombre a buscar. La información del usuario se guarda en el _localStorage_ después de realizar el login.
## Manejo de errores
Para el manejo de errores se está empleando la librería _werkzeug_ que facilita la detección de errores específicos y los redirecciona a una ruta predeterminada.
