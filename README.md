<h1 align='center'>
<b>Todo Peliculas</b>
</h1>

![Portada](Dataset/portada.jpg)

### Tabla de contenido
1. [Introducción](#Introduccion)
2. [Requisitos](#Requisitos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Uso y Ejecución](#uso-y-ejecución)
5. [Datos y Fuentes](#datos-y-fuentes)
6. [Metodología](#metodología)
7. [Resultados y Conclusiones](#resultados-y-conclusiones)
8. [Contribución y Colaboración](#contribución-y-colaboración)
9. [Licencia](#licencia)

### Introduccion
Este proyecto genera una aplicacion que responde a consultas sobre peliculas. Si te gusta un actor podes consultar las peliculas en la que participó. Lo mismo podes consultar todas las peliculas que dirigió tu director favorito. Además te recomienda la cantidad de peliculas que elijas y que sean similares a una pelicula que hayas visto y te gustó. Esto es posible gracias a la gran base de datos con la que cuenta y al uso de la IA para obtener las peliculas mas parecidas.
Para hacer uso de esta aplicacion puedes utilizar el siguente link [LINK API](https://api-peliculas-pnfg.onrender.com/docs) o clonar el repositorio en tu computadora local. 

### Requisitos
Para que la API funcione correctamente deberas tener instaladas las siguientes aplicaciones Python:
#### fastapi, uvicorn, scikit-learn, scipy, pandas, numpy

### Pasos de instalación: 
Realizar los siguientes pasos desde una terminal: 
1. Clonar el repositorio: `git clone [https://github.com/usuario/proyecto-ventas-ropa.git](https://github.com/LauchaLogico/T1_Simontacchi.git)`
2. Creo un entorno virtual: virtualenv nombre_del_entorno
3. Activo el entorno virtual: nombre_del_entorno\Scripts\activate
4. Instalo las aplicaciones: pip install -r requirements.txt
5. Para correr el servidor de uvicorn: uvicorn main:app --reload  
