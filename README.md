Se debe desarrollar sitio web en el que se registran pedido de préstamos de usuarios que acceden a el.
El usuario no necesita registrarse para solicitar un préstamo.
Para definir si al usuario se le aprueba o no el préstamo usaremos una API definida debajo.

endpoint: https://api.moni.com.ar/api/v4/scoring/pre-score/[dni]
tenés que pasarle en los headers credential: ZGpzOTAzaWZuc2Zpb25kZnNubm5u
ejemplo: curl https://api.moni.com.ar/api/v4/scoring/pre-score/30156149 -H "credential: ZGpzOTAzaWZuc2Zpb25kZnNubm5u"

El formulario de pedido de préstamos, el usuario debe ingresar dni, nombre y apellido, genero, email y monto solicitado.
El usuario luego de ingresar los datos debe recibir la respuesta negativa o positiva en la misma página que ingresó sus datos.
Contemplar casos de datos ingresados con errores.

También se debe desarrollarse un sitio de administración en el que se puedan ver los pedidos de préstamo, con la opción eliminarlos. A este sitio solo pueden acceder usuarios administradores. No usar admin de Django.

## Requeriments
* docker
* docker-compose

## Create environment
```
docker-compose build
docker-compose up
CTRL + C
docker-compose web python manage.py loaddata genders
docker-compose web python manage.py createsuperuser
```

## Run Server
```
docker-compose up
```

## Test
```
docker-compose exec web python manage.py test
```
