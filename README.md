# SegRedP4-DockerHTTPS
El proyecto consiste en una api REST encargada de autenticación y gestión de ficheros.
El protocolo que usa es HTTPS por lo que hace uso de certificados para la seguridad en la comunicación web.
La api se encuentra distribuida en dockers en los que hay varios nodos:

    - **router**: se encuentra en las distintas redes y las comunica, también incluye el firewall con las políticas de seguridad
              entre las que se encuentran permitir la comuniciación entre los puertos que usamos para el HTTPS (5000) los 
              puertos SSH y demás.
              
    - **jump**: este nodo servirá para acceder a work, será la única entrada a los nodos y el router traducirá su IP
    
    - **work**: desde este nodo, que se llega a través de jump únicamente, se accede al resto de nodos
    
    - **broker, auth, files**: son los nodos que ejecutan el servidor distribuido
    
Hay tres tipos de usuarios:

    - **dev**: que solo tiene acceso al nodo work
    
    - **op**: que tiene acceso a todos los nodos y a superusuario
    
    - **jump**: solo es accesible desde el exterior y para realizar el salto al nodo work
    
Hay tres redes:

    - **dmz**: en ella están el broker y jump ya que son los únicos nodos que se comunican con el exterior
    
    - **srv**: en ella están auth y files que no tienen comunicación con el exterior
    
    - **dev**: donde se encuentra el nodo work
    
Para acceder a los nodos será mediante SSH usando claves públicas y privadas, una para *dev* y otra para *op*, y SSH solo puede
    estar permitido para las restricciones nombradas (dev solo puede acceder a work y op a todo, ambos median jump a work)

Para instalar y ejecutar el proyecto, en el directorio dockers hay un archivo Makefile con el que instalar y ejecutar la api. Comandos make del Makefile:

    - **build**: crea las imágenes de los nodos
    
    - **network**: crea las redes para los dockers
    
    - **containers**: ejecuta primero los comandos anteriores y después crea los contenedores con sus respectivas imágenes y conectándolos a las redes que corresponden
    
    - **remove**: para y borra los contenedores
    
    - **clean**: borra archivos backup no necesarios
    
    - **run_tests**: ejecuta el test.py que también se encuentra en el directorio y que mandará distintas peticiones a la api

Antes de instalar y ejecutar el proyecto es necesario añadir las claves privadas de los usuarios op y dev al agente ssh o crear unas nuevas, las claves se encuentran en docker/assets/ y si se crean unas nuevas hay que cambiar en /docker/jump/authorized_keys las que contienen por las nuevas públicas generadas. Los certificados no hace falta cambiarlos ni generarlos pero si se generan en el apartado "Common Name" que pide hay que poner "*myserver.local*" "*auth.local*" y "*file.local*" para los certificados de broker, auth y files respectivamente.

Para acceder a work con un usuario se ejecuta con el comando "*ssh -Ai <ruta a la clave privada del usuario> -J jump@172.17.0.2 <usuario>@10.0.3.3*"
y desde work si has entrado como usuario "op" podrás acceder al resto de nodos con el comando "*ssh op@<ip del nodo al que se quiere acceder*>

Para probar el proyecto de forma rápida en el directorio dockers ejecuta "make containers" y después "make run_tests", es posible que si no tienes configurado los dockers para usarlo como superusuario tengas que ejecutarlos como superusuario, el archivo test.py utiliza una dirección "*myserver.local*" que en local traduce a 172.17.0.2, para ejecutarlo se pueden hacer dos opciones; o bien añadir en etc/hosts una línea en la que ponga "172.17.0.2  myserver.local" o bien cambiar en el código de test.py "myserver.local" por esta dirección al principio del código donde se especifica la URL.
