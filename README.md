# Backend
## Objetivos
Crear un API que se conecte a la base de datos de la aplicación, realizando las funciones especificadas en el reto.

## Usar la API
Primero se debe crear el entorno virtual y usarlo con los comandos:
~~~bash
python3 -m venv venv
source venv/bin/activate
~~~

Luego se debe instalar las dependencias con el comando:
~~~bash
pip install -r requirements.txt
~~~

Por ultimo crearemos el servidor con el comando:
~~~bash
uvicorn main:app
~~~

**Para probarla se deberá consultar el siguiente link:** [http://127.0.0.1:8000/api/v1/docs](http://127.0.0.1:8000/api/v1/docs)

## Referencias
[Planeación](https://miro.com/app/board/uXjVO_NmmaE=/?share_link_id=466171238038) - Miro board

[Diagrama entidad relación](SS-20220731171812.png)