# KeyBase-Git

Este programa sirve para subir a keybase de forma automatica y periodica, proyectos de git guardados en el ordenador,
con el fin de que si os roban el ordenador el código fuente que desarrollemos este encriptado en los servidores de keybase y no en vuestros ordenadores, que por lo general son fáciles de hackear y de acceder a la info que teneis dentro sin el pin.

### Requirements
- Tener KeyBase instalado y estar loggeado
- Python >= 3.7
- No tiene dependencias externas por lo que no hay que instalar nada con pip (todo módulos itegrados de python)

### Instalación
- Para que funcione, tenéis que crearos una cuenta de keybase, y dejar habilitada la opción en settings de nunca cerrar sesión (si os roban el ordenador se puede cerrar la sesión desde otro dispositivo y solo pueden acceder a vuestros datos si están conectados a internet (no habilitéis la opción de sincronizar datos en vuestras carpetas de keybase, ya que esto hace que se pueda acceder a vuestros datos de keybase de forma offline y no queremos eso)).
- También tenéis que activar la opción de abrir keybase on startup, para que se os inicie cuando encendáis el ordenador (permite que el programa pueda interactuar con keybase sin que toquéis nada)
- De normal estas dos opciones que os he comentado vienen activadas ya por defecto, pero por si acaso no, activadlas

### Intalar de forma Global 
- Para acceder al script de forma global desde cualquier path y sin tener que ejecutar 'python ...' teneis que ejecutar el instalador correspondiente a vuestro sistema operativo -> 'scripts/[win o posix]/installer[.bat o .sh]' (posix = mac y linux) (en caso de posix, ya están dados los permisos de ejecución a los archivos). El script os pedirá permisos de administrador para que se pueda copiar el script 'kbase-git.[OS]' en una ruta que esté añadida en el PATH del sistema por defecto, 'C:\Windows\System32' (windows) y '/usr/local/bin' (linux y mac).
- En la instalación se os creará un archivo en 'configs/[vuestro username de keybase].json' donde podréis poner los paths que quereis que se os suban directamente a keybase (mirar 'example.json'). También se os creará una carpeta personal con vuestro nombre de usuario automáticamente en keybase dentro de '/keybase/team/skin4cloud/kbase-git_uploads'
- Para comprobar que esta bien instalado, ejecutad 'kbase-git' desde una terminal de comandos para desplegar la ayuda del programa.

### Modo de uso
    - upload ['--config-paths']
    - download ['--config-paths']
Si se pone ['--config-paths'], en vez de mover o descargar el directorio en el que os encontreis, subirá/descargará todos los paths a keybase que hayais puesto en el archivo '[nombre usuario].json'
```
{
    "paths":[
        "C:\\example\\for\\windows\\path",
        "/example/for/posix/path"
    ]
}
```

### Añadir Task en el ordenador
- Para que se ejecute todos los días varias veces de forma automática del script, hay que crear un TASK en el ordenador que ejecute 'kbase-git --config-paths --counter' (ya veremos como poneros el task a cada uno (en Windows es fácil y en MAC o Linux habrá que investigar).