# KeyBase-Git

Este programa sirve para subir a keybase de forma automatica y periodica, proyectos de git guardados en el ordenador,
con el fin de que si os roban el ordenador el código fuente que desarrollemos este encriptado en los servidores de keybase y no en vuestros ordenadores, que por lo general son fáciles de hackear y de acceder a la info que teneis dentro sin el pin.

### Modo de uso
    - upload ['--config-paths']
    - download ['--config-paths']
Si se pone ['--config-paths'], en vez de mover o descargar el directorio en el que os encontreis, subirá/descargará todos los paths a keybase que hayais puesto en el archivo 'config.json'
```
{
    "paths":[
        "C:\\example\\for\\windows\\path",
        "C:/example/for/posix/path"
    ]
}
```

### Requirements
- Python >= 3.7
- No tiene dependencias externas por lo que no hay que instalar nada con pip (todo módulos itegrados de python)

### Instalación
- Para que funcione, tenéis que crearos una cuenta de keybase, y os recomiendo dejar habilitada la opción en settings de nunca cerrar sesión (aunque este programa tiene implementado la opción de pediros iniciar sesión, no es perfecta y a veces hay que reintentar varias veces para que funcione: mejor que esté siempre iniciada) (si os roban el ordenador se puede cerrar la sesión desde otro dispositivo y solo pueden acceder a vuestros datos si están conectados a internet (no habilitéis la opción de sincronizar datos en vuestras carpetas de keybase, ya que esto hace que se pueda acceder a vuestros datos de keybase de forma offline y no queremos eso)).
- También tenéis que activar la opción de abrir keybase on startup, para que se os inicie cuando encendáis el ordenador (no se os abre la interfaz de usuario, solo se inicia internamente y permite que el programa pueda interactuar con keybase sin que toquéis nada)
- De normal estas dos opciones que os he comentado vienen activadas ya por defecto, pero por si acaso no, activadlas
- A continuacion abrir el archivo 'kbase-git.py' y poned vuestro nombre de usuario en la variable 'username'

### Intalar de forma Global 
- Para acceder al script de forma global desde cualquier path y sin tener que ejecutar 'python ...' teneis que coger el script que esta en 'scripts/[OS]/kbase-git.[OS]' correspondiente a vuestro systema operativo (windows o posix (mac y linux)), editar el path que hay dentro poniendo la ruta absoluta de donde guardéis el archivo 'kbase-git.py' y ejecutar el instalador correspondiente 'installer.[OS]' (en caso de Posix, ya están dados los permisos de ejecución a los archivos). Tendrés que dar permisos de administrador para que se pueda copiar el script 'kbase-git.[OS]' en una ruta que esté añadida en el PATH del sistema, C:\Windows\System32 (windows) y /usr/local/bin (linux y mac).

Linux y Mac
```
#!/bin/bash

python3 /path/to/kbase-git.py $@
```
Windows
```
@echo off

py "C:\\absolute\\path\\to\\kbase-git.py" %*
```
- Para comprobar que esta bien instalado, ejecutad 'kbase-git' desde una shell en un path distinto al del proyecto y debería desplegaros la ayuda del programa.

### Añadir Task en el ordenador
- Para que se ejecute todos los días varias veces de forma automática del script, hay que crear un TASK en el ordenador que ejecute 'kbase-git --config-paths --counter' (ya veremos como poneros el task a cada uno (en Windows es fácil y en MAC o Linux habrá que investigar).