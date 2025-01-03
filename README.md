<h1 align='center'>
<b>Todo Peliculas</b>
</h1>

![Portada](Dataset/portada.jpg)

### Tabla de contenido
1. [Introducción](#Introduccion)
2. [Requisitos](#Requisitos)
3. [Pasos de intalacion](#Pasos-de-intalación)
4. [Estructura](#estructura)
5. [Autor](#Autor)

### Introduccion
Este proyecto genera una aplicacion que responde a consultas sobre peliculas. Si te gusta un actor podes consultar las peliculas en la que participó. Lo mismo podes consultar todas las peliculas que dirigió tu director favorito. Además te recomienda la cantidad de peliculas que elijas y que sean similares a una pelicula que hayas visto y te gustó. Esto es posible gracias a la gran base de datos con la que cuenta y al uso de la IA para obtener las peliculas mas parecidas.
Para hacer uso de esta aplicacion puedes utilizar el siguente link [LINK API](https://api-peliculas-pnfg.onrender.com/docs) o clonar el repositorio en tu computadora local. 

### Requisitos
Para que la API funcione correctamente deberas tener instaladas las siguientes aplicaciones Python:
#### _fastapi, uvicorn, scikit-learn, scipy, pandas, numpy_

### Pasos de instalación: 
Realizar los siguientes pasos desde una terminal: 
1. Clonar el repositorio: git clone https://github.com/LauchaLogico/T1_Simontacchi.git
2. Creo un entorno virtual: virtualenv nombre_del_entorno
3. Activo el entorno virtual: nombre_del_entorno\Scripts\activate
4. Instalo las aplicaciones: pip install -r requirements.txt
5. Para correr el servidor de uvicorn: uvicorn main:app --reload
6. se te proporcionará en enlace, "http://..." hacer click en el o copiar y pegar en un navegador y agregar "/docs" al final

### Estructura
- `Dataset/`: Carpeta que ontiene los archivos de datos utilizados para realizar las consultas.
- `notebooks/`: Jupyter notebooks con el análisis.
- `main.py`: Código fuente.
- `reports/`: Informes y visualizaciones.
- `README.md`: El archivo que estás leyendo.
- `requerimens.txt`: archivo que contiene las librerias utilizadas en el código fuente.

### Autor:
Laucha Logico - Contacto: [LinkedIn](www.linkedin.com/in/lautaro-simontacchi-75b77580). [Instagram](https://www.instagram.com/laucha_logico/)


