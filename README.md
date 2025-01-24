# Prueba Técnica Backend - IOTA

# Impact

Andrés Jiménez García
24/01/
Se desarrolla la autenticación OAuth2 en GitHub empleando Django Rest Framework, en
donde finalmente se puede consultar datos públicos del usuario de GitHub como por
ejemplo su nombre de usuario. En este documento, se presenta un informe sobre la
construcción e implementación de la API.

## Inicio del proyecto

El proyecto se inicia utilizando Python 3.11 y django 5.1.5, no se toman las últimas
versiones principalmente para asegurar la compatibilidad de las herramientas empleadas.
En ocasiones suelen existir problemas al utilizar las versiones más recientes, por lo que por
agilidad y por haberla trabajado previamente, se toman dichas versiones. Adicionalmente,
para conservar un ambiente de desarrollo replicable, se utiliza un virtual environment y se
guardan las librerías utilizadas en el archivo _requirements.txt_ con sus respectivas versiones.
Como base de datos se utiliza PostgreSQL en su versión 17 en el servicio _Amazon
Relational Database Service_ (RDS) de AWS, esto es simplemente por facilidad de crear
rápidamente el servidor donde se ejecuta la base de datos y evitar configuraciones e
instalaciones locales para agilizar. Sin embargo, muy bien se podría levantar un servidor
local realizando la instalación en el sistema o empleando imágenes Docker por ejemplo,
aunque la nube por escalabilidad y evitar la administración del entorno de ejecución es lo
recomendado. Así mismo, se selecciona PostgreSQL por su eficiencia y robustez, además
por ser una de las bases de datos más usadas, tiene buena documentación, soporte y
confiabilidad, sumado a que personalmente ya se ha utilizado en proyectos anteriores.
Una vez establecida la base de datos, se realiza la conexión entre django y la base datos
empleando _psycopg2_ , esto se realiza principalmente como estándar, este adaptador es
ampliamente usado y tiene buen soporte.

# Autenticación Oauth2 en GitHub

Para la autenticación se emplea la librería _requests_oauthlib_ , principalmente por
recomendación de la prueba técnica y por la revisión que se realizó previo a emplearla, ya
que se encontró buena documentación y buenas métricas de seguimiento en su repositorio
de GitHub. Durante la búsqueda de otras alternativas, se encontraron otras librerías que
presentaban también un alto uso para el desarrollo de proyectos en Python y con buena
documentación, sin embargo, se le dio mayor relevancia a _requests_oauthlib_ , puesto que


presenta mejor desempeño y compatibilidad al estar basada en la librería _requests_ la cual
es la librería por excelencia para realizar consultas.
Para la creación de la API se revisó el funcionamiento como tal de OAuth2 en general, la
documentación de request_oauthlib y de OAuth en GitHub, donde se indican los procesos
recomendados para realizar la autenticación adecuadamente.
Una vez realizado el proceso de autenticación, se emplea una consulta para extraer la
información básica del usuario como se indica en la documentación de la API GitHub.

# Testing

Para corroborar el funcionamiento de los servicios para futuras adecuaciones del código, se
emplea la librería _requests-mock_ para realizar pruebas unitarias. Esto puede encontrarse en
el proyecto _github_auth/tests.py_ , en donde mediante la librería se interceptan y simulan
respuestas de las consultas HTTP a la API de autenticación de GitHub.

# Modo de uso

Suponiendo un entorno de desarrollo local, la URL base sería: [http://localhost:8000/](http://localhost:8000/) Y a
partir de esto, se pueden consultar los servicios indicados en la tabla 1.
Tabla 1. Servicios de la API para la autenticación OAuth2 en GitHub
| **Ruta**  | **Método** | **Descripción**                                                                  | **Response**                                                    |
|-----------|------------|----------------------------------------------------------------------------------|-----------------------------------------------------------------|
| login/    | GET        | Ruta para iniciar sesión, se redirecciona a la página de autorización de GitHub  | HTTP Status 302 Redirect                                        |
| callback/ | GET        | Página de redirección cuando el inicio de sesión sea exitoso                     | HTTP Status 200 Body: {'message': 'Successfully authenticated'} |
| profile/  | GET        | Consulta la información del usuario en el endpoint de GitHub                     | HTTP Status 200 [Body Example](https://docs.github.com/en/rest/users/users?apiVersion=2022-11-28)                                    |
| logout/   | GET        | Elimina el token de la sesión                                                    | HTTP Status 302 Redirect                                        |

# Conclusiones y trabajos futuros

Se implementó la autenticación OAuth2 adecuadamente para una API Rest construida en
django, lo que permite acceder a la información del usuario correctamente. Esto es
resultante del análisis desarrollado para la ejecución adecuada, en donde se tuvo en cuenta
las recomendaciones dadas en las documentaciones de las librerías empleadas. Dichas
librerías fueron seleccionadas de acuerdo al soporte que tienen, seguimiento por la
comunidad y calidad de la documentación, lo que permite que a futuro la implementación


desarrollada pueda ser sostenida y mejorada fácilmente. A demás que su conexión con
AWS permite tener mejor escalabilidad, mayor rendimiento y seguridad, por lo que sé
trabajan con metodologías que son bien acogidas por la comunidad de desarrolladores
como AWS RDS y PostgreSQL. Adicionalmente, se considera que los servicios podrían
fallar en algún momento con implementaciones futuras o incompatibilidad entre módulos,
por lo que se emplean pruebas unitarias para asegurar el correcto funcionamiento de los
servicios desarrollados antes de lanzar la aplicación.
Como trabajos futuros se podría utilizar la información retornada por la API de GitHub para
conectarla a una aplicación que permita mostrar usuario, avatar, etc. Además de tener la
posibilidad de unirse con la lógica propia de alguna aplicación para manejar su inicio de
sesión y de esta forma, tener control sobre las acciones del usuario para guardar,
mostrar/ocultar información, todo esto, implementando tablas adicionales para almacenar
estos datos.