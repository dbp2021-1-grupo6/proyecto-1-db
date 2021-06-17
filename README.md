# Proyecto 1 - Parte Web (U - Games)
**Integrantes**
- Andrés Lostaunau
- Sebastián Calle
- Esteban Vásquez
## Descripción
El proyecto simula una página web de compras de juegos en línea en el cuál también cada usuario tiene acceso a un inventario individual. También simula transacciones de compra y de adicción	 de fondos.
## Objetivos
- Los clientes deben ser capaces de crear una cuenta y usarla pasando por una autenticación.
- Al realizar una compra la transacción debe ser integra, de modo que no pueden haber ningún tipo de anomalías en la compra.
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
## Hosts
Todas las operaciones se están realizando en _localhost:8080_ por el momento.
## Forma de autenticación
Para el login el usuario es autenticado buscando la información en la base de datos. El nombre de usuario es un atributo _unique_ por ende solo puede existir un usuario con el nombre a buscar. La información del usuario se guarda en el _localStorage_ después de realizar el login.
## Manejo de errores
Para el manejo de errores se está empleando la librería _werkzeug_ que facilita la detección de errores específicos y los redirecciona a una ruta predeterminada.
