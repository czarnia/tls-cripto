# tls-cripto
Repositorio para el trabajo final de Criptografía y Seguridad Informática, contiene las pruebas de concepto utilizadas para la realización del mismo.

![Poodle Attack in Dockers!](https://raw.githubusercontent.com/czarnia/tls-cripto/Poodle-PoC/poodle-attack.gif)

## Requerimientos

- Docker
- Docker-compose

## Modo de uso

Al ejecutar el script ``tls_demo_up.sh`` se hará un _build_ de dos imágenes de Docker, una para el servidor y una para el cliente, luego de esto se levantarán dos _containers_, uno con cada imágen.

Se tienen tres pruebas de concepto: 

- Cliente y servidor sin TLS.
- Cliente y servidor con TLS.
- Ataque POODLE.

Para usar las mismas se debe entrar a los containers con ``docker exec -it <nombre_del_container> /bin/sh`` y correr los distintos archivos python, siempre ejecutando primero el servidor y luego el cliente. Los resultados se verán por pantalla.
Para eliminar los containers basta con ejecutar ``docker-compose down`` en una terminal parada dentro de la carpeta _root_ de este proyecto.