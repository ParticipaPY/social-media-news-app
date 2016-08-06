# Social Media News App
Social Media News App es una aplicación web de código abierto que extrae automáticamente las noticias publicadas por los principales medios de comunicación nacionales en sus perfiles oficiales de las redes sociales Facebook y Twitter, para esto utiliza las APIs ofrecidas por estas redes sociales.

Los publicaciones obtenidas son almacenadas en archivos CSV, un formato simple pero estructurado, independiente de una herramienta específica y que puede ser fácilmente exportado a Microsoft Excel, Google Spreadsheets o incluso a una base de datos, facilitando así su posterior análisis.

##Formato de Salida
Como resultado de la ejecución de la aplicación se obtiene como salida un archivo CSV por cada una de las fuentes de noticias. Cada archivo CSV contiene la siguiente estructura: 

 - **source**: nombre de la fuente.
 - **created_time**: timestamp de creación del post de Facebook o tweet.
 - **text**: contenido textual del post/tweet.
 - **url**: del post/tweet en su respectiva plataforma.
 - **likes/favorites**: cantidad de votos positivos recibidos, según la red social.
 - **shares/retweets**: cantidad de veces que se compartió, según la red social.
 - **comments/replies**: cantidad de comentarios, según red social.

Estos campos fueron seleccionados con el fin de ofrecer un formato de salida homogéneo independiente de las variaciones que puedan tener las publicaciones de Facebook con respecto a las de Twitter.


##Componentes
La aplicación consiste en tres componentes, escritos en el lenguaje de programación  Python (http://www.python.org):

 1. **Configuración del programa**: Consiste en un módulo Python en el que los usuarios de la aplicación deben establecer los valores de los parámetros necesarios para el funcionamiento de los otros dos componentes.
 2. **Extractor de Noticias de Facebook**: obtiene los posts de fanpages de Facebook ordenados cronológicamente de más reciente a más antiguo.
 3. **Extractor de Noticias de Twitter**: descarga los tweets de cuentas públicas de Twitter.

###Configuración del Programa
Los parámetros de funcionamiento de los componentes se definen mediante la declaración de  las siguientes variables:

 1. las fuentes (cuentas) de dónde obtener los posts/tweets, indicando el nombre y el ID de la mismas en un diccionario: 	
 * `facebook_sources = {‘ABC Color’: ‘280037675322’}`
 * `tw_sources = {‘ABC Color’ : 28191953}`
 2. la antigüedad máxima que pueden tener (hasta qué punto del pasado seguir extrayendo las publicaciones) en cantidad de días. Es una variable llamada `days` y su valor es un entero.
 3. los tokens de acceso necesarios para poder utilizar la API de las redes sociales mencionadas. 

###Extractor de noticias de Facebook
Consiste esencialmente en un ciclo que itera sobre cada una de las fuentes de búsqueda. Para cada una de ellas hace una llamada a la API de Facebook solicitándole los posts publicados por dicha fuente desde el momento en que se efectúa la búsqueda hasta la fecha especificada en la variable `days`. 

La API no devuelve todos los posts solicitados en una sola llamada sino que la respuesta llega paginada. Esto es, un ciclo anidado se encarga de llamar sucesivamente a la API de Facebook solicitando la siguiente página hasta que no haya más posts publicados por esa fuente en el rango de fecha especificado.

Posteriormente, cada post individual es procesado para obtener los campos del formato de salida mencionados anteriormente. Por ej:. Todo el texto que podemos leer en un post de facebook desde su página web es retornado por la API en distintos campos (como título descripción y mensaje). Nuestra aplicación concatena dichos textos para formar un único cuerpo de texto, ya que de esa manera se obtiene un formato más parecido al de un tweet (que tiene un único campo de texto) y de esa forma obtenemos una salida homogénea entre redes sociales distintas.

###Extractor de noticias de Twitter
Al igual que su contraparte de Facebook, el Extractor de Noticias de Twitter consiste en un ciclo que itera sobre cada fuentes de noticias para descargar sus tweets y crea un archivo CSV de salida para cada una de estas. Sin embargo, existen diferencias tres aspectos fundamentales:

La API de Twitter no permite especificar el rango de fechas de los tweets solicitados por lo que nuestra aplicación realiza un ciclo que en cada iteración solicita un conjunto de tweets (190 cada vez para ser exactos, según un límite establecido por la API), de más recientes a más antiguos, hasta que encuentra alguno cuya fecha de publicación salga del rango fijado por el usuario. 

La paginación de la respuesta no viene implementada por la API de Twitter y debe controlarse de manera manual desde nuestra aplicación. Para ello nos valemos de los identificadores de tweets: en cada llamada recibimos un conjunto de 190 tweets, el último tweet de cada conjunto es el más antiguo del conjunto, por lo que para el siguiente conjunto solicitado le indicamos a la API que nos retorne sólo aquellos tweets más antiguos a éste último. Para indicarle este límite, cada llamada a la API recibe como parámetro el identificador del último tweet del conjunto anterior.

La cantidad de replies de un tweet no es una información retornada por la API. Por lo que para calcularla se utiliza una función auxiliar que realiza web-scrapping sobre el html retornado por la invocación de la url de cada tweet. Esta función descarga el código html del tweet, lo analiza en búsqueda de las secciones correspondientes a comentarios y realiza un conteo de cada comentario encontrado.

## Instalación

 1. Clonar el repositorio 
`git clone https://github.com/ParticipaPY/social-media-news-app.git`

 2. Ir a la carpeta del repositorio y ejectuar
`pip install -r requirements.txt` 
para instalar las dependencias.

 3. Establecer los siguientes parámetros de configuración en el archivo _configuration_file.py_ 	 
 * las **fuentes** (cuentas) de dónde obtener los posts/tweets, indicando el nombre y el ID de la mismas en un diccionario de python.
	 * facebook_sources = {'ABC Color': '280037675322'}
	 * tw_sources = {'ABC Color' : 28191953}
 * la **antigüedad** máxima que pueden tener (hasta que punto del pasado seguir trayendo las publicaciones) en cantidad de días. Es una variable de python llamada _days_ y su valor es un entero.
 * los **tokens de acceso** necesarios para poder utilizar las API de las redes sociales mencionadas. Más adelante se detallan cuáles son y cómo se obtienen

###ID de Fanpages de Facebook
Para obtener el ID de una fanpage podesmos acceder a [este sitio web](http://findmyfbid.com/) en el que pegamos la url de una fanpage determinada y presionamos _Find numeric ID_. El valor obtenido debe ser copiado al diccionario de python _facebook_sources_ como un string, cuya clave dentro del diccionario sería el nombre de la fuente.
###ID de cuentas de Twitter
Para obtener el ID de las cuentas, cuyos tweets se quieren capturar, se puede acceder al [siguiente enlace](https://tweeterid.com/) en el que basta introducir el usuario (Ej.: @ABCDigital)

###Tokens de Acceso
Los tokens de acceso son identificadores en forma de cadena de caracteres que nos permiten realizar llamadas a la API de las plataformas sociales. Obtenerlos es una tarea obligatoria para el funcionamiento de la aplicación .

####Facebook
En el caso de Facebook necesitamos un string dentro de _configuration_file.py_, llamado _facebook_access_token_.

Para poder obtenerlo debemos seguir los siguientes pasos:

 1. Ir a [https://developers.facebook.com/](https://developers.facebook.com/), e iniciar sesión. Para registrar nuestra cuenta de facebook como developer debemos ingresar un número de teléfono válido.
 2. Crear una aplicación yendo a _Mis Aplicaciones_ => _Añadir una nueva aplicación_. Seleccionar la opción _WWW_ y completar la información requerida.
 3. Una vez ha sido creada, la aplicación podrá ser accedida desde _Mis Aplicaciones_. En la _Página Principal_ del _Panel_ de la aplicación (lo primero que vemos al seleccionar la aplicación) se encuentran los datos que necesitamos para el access token. Estos son:
	* Identificador de la aplicación (AppID).
	* Clave secreta de la aplicación. (AppSecret). Hay que introducir la contraseña de facebook para poder visualizar el contenido de este campo.
 4. El valor de la variable _facebook_access_token:_ será:
	* facebook_access_token = "AppID|AppSecret"
 5. Alternativa: Para no crear la aplicación se puede acceder directamente al [explorador de la api](https://developers.facebook.com/tools/explorer) y pulsar el botón _Get Token_ => _Get User Access Token_ => _Get Access Token_. El valor obtenido en el campo _Identificador de Acceso_ puede ser utilizado para el string _facebook_access_token_. Sin embargo, este tiene una duración corta de 1 o 2 horas de validez. Por lo que se sugiere usar los pasos descritos anteriomente para obtener un token de larga duración que permita ejecutar el programa sin la limitación del tiempo.

#### Twitter
En caso de Twitter son cuatro los strings necesarios dentro de _configuration_file.py_:

1. tw_access_token
2. tw_access_secret
3. tw_consumer_key
4. tw_consumer_secret

Para obtener los tokens de acceso necesarios para hacer uso de la API de Twitter debemos seguir los siguientes pasos:

 1. Crear una aplicación, para ello debemos acceder al siguiente enlace  https://dev.twitter.com/apps/new, completar los campos necesarios, aceptar las condiciones de uso "Twitter Developer Agreement" (TDA) y presionar el botón *Create your Twitter Application*
 2. Una vez creada la aplicación accedemos a la pestaña *Keys and Access Tokens*, y en la sección *Application Settings* obtenemos: 
	 * 	Consumer Key (API Key), correspondiente a la variable _tw_consumer_key_.
	 * 	Consumer Secret (API Secret), correspondiente a la variable _tw_consumer_secret_.
 3. Finalmente, vamos a la sección *Your Access Token* y pulsamos el botón *Create my access token* , con el ello obtenemos:
	 * 	Access Token, correspondiente a la variable _tw_access_token_.
	 * 	Access Token Secret, correspondiente a la variable _tw_access_secret_.

	
##Uso

Una vez realizados los pasos de instalación cualquiera de los dos scripts de búsqueda puede ser ejecutado desde una interfaz de línea de comandos de la siguiente manera:
`python facebook_search.py`

La duración de la ejecución dependerá del valor de la variable _days_ pero sobre todo de la cantidad de publicaciones hechas en ese lapso de tiempo por cada fuente. Sintiendose más este efecto Twitter que en Facebook pudiendo llegar a varias horas por cada fuente si hablamos de 3200 tweets alcanzados (Véase Limitaciones).

Si se desea agregar o modificar las fuentes consultadas simplemente pueden editarse las variables correspondientes en _configuration_file.py_ antes de ejectuar los scripts.



##Limitaciones

El proceso de obtención de los identificadores (ID) de las fuentes definidas en el archivo de configuración del programa es un proceso manual, en el cual, por cada una de las fuentes se debe acceder a diferentes sitios (Find my Facebook ID, en el caso de Facebook y TweeterID, en el caso de Twitter) para la obtención de sus respectivos IDs.

Si bien la variable `days` , definida en la configuración del programa, indica la antigüedad máxima que tendrán los tweets obtenidos, la API de Twitter cuenta con una limitación establecida para retornar un máximo de 3200 tweets recientes. Esto implica que si se llega a dicho límite antes de alcanzar la antigüedad deseada, entonces el proceso se detendrá antes de alcanzarla.

Además, como se mencionó en la descripción del Extractor de Noticias de Twitter, para calcular la cantidad de replies de un tweet se utiliza una técnica de web-scrapping (ya que dicho dato no es devuelto por la API) y esta función representa un cuello de botella en cuanto a velocidad de ejecución debido a la sobrecarga que implica descargar cada tweet.

##Futuras Mejoras
Una mejora propuesta consiste en Implementar una interfaz gráfica web para configurar y utilizar la herramienta. Actualmente solo puede ser utilizada a través de una interfaz de línea de comandos, y los resultados de salida deben procesarse y visualizarse mediante algún otro programa como un editor de planillas electrónicas. Además del uso y de la visualización de resultados, la configuración es otro aspecto que se beneficiará de una interfaz gráfica, ya que actualmente los parámetros deben ser editados en un archivo de texto.

Otra posible mejora es implementar un sistema de cacheo para reducir las llamadas a las APIs de las redes sociales. Esto permitiría solicitar solamente aquellos tweets/posts que no se hayan solicitado previamente reduciendo el tiempo de respuesta y haciendo que se alcance más lentamente el límite que la API de Twitter posee.

Implementar técnicas de machine learning para diseñar un sistema de clasificación, que identifique categorías de noticias relacionadas dependiendo del contenido de cada una de las publicaciones (por ejemplo: Política, Educación, Sociales, etc ).

