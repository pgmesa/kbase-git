# KeyBase-Git

Este programa sirve para subir a keybase de forma automatica y periodica, proyectos de git guardados en el ordenador,
con el fin de que si os roban el ordenador el código fuente que desarrollemos este encriptado en los servidores de keybase y no en vuestros ordenadores (fácil de hackear y de acceder a la info que teneis dentro sin el pin).

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
- Para que funcione, tenéis que crearos una cuenta de keybase, dejar habilitada la opción de settings de nunca cerrar sesión (si os roban el ordenador se puede cerrar la sesión desde otro dispositivo y solo pueden acceder a vuestros datos si están conectados a internet (no habilitéis la opción de sincronizar datos en vuestras carpetas de keybase, ya que esto hace que se puede acceder avuestros datos de keybase de forma offline y no queremos eso)).
- A continuacion abrir el archivo 'kbase-git.py' y poned vuestro nombre de usuario en la variable 'username'
- Para acceder al script de forma global desde cualquier path y sin tener que ejecutar 'python ...' teneis que coger el script que esta en 'scripts/posix/' correspondiente a vuestro systema operativo (windows o posix (mac y linux)), editar el path que hay dentro poniendo la ruta absoluta de donde guardeis el archivo 'kbase-git.py' y poner el script en la variable PATH de vuestro ordenador para poder ejecutarlo de forma global.
- Para que se ejecute todos los días varias veces la subida automática del script haya que crear un TASK en el ordenador ejecuter 'kbase-git --config-paths' (ya veremos como poneros el task a cada uno)