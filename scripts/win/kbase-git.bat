@echo off

@REM Comprobamos que el disco esta montado
if exist K: (
    echo ERROR: Keybase K:\ unit is not mounted
    exit 1
)

@REM Comprobamos que tenemos conexion a internet y que tenemos acceso al team Skin4Cloud
if exist K:\team\skin4cloud (
    echo ERROR: You seem to be offline or not in Skin4Cloud keybase team
    exit 1
)

@REM Vemos el nombre de usuario
FOR /F "tokens=*" %a in ('keybase whoami') do SET name=%a
@REM Creamos la carpeta correspondiente al usuario
keybase fs mkdir /keybase/team/skin4cloud/desarrollo/utils/kbase-git/uploads/%name%
@REM Creamos el fichero de configuracion base del usuario
set fname=/keybase/team/skin4cloud/desarrollo/utils/kbase-git/configs/%name%.json
keybase fs read %fname%
if %errorlevel% NEQ 0 (
    keybase fs cp /keybase/team/skin4cloud/desarrollo/utils/kbase-git/configs/example.json %fname%
)

py "K:\team\skin4cloud\desarrollo\utils\kbase-git\kbase-git.py" %*
