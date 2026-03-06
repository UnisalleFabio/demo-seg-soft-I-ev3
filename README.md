# Ejemplo guiado en Python para EV3

Esta rama contiene una version intencionalmente insegura de un portal academico pequeno.

El objetivo no es mostrar "codigo feo", sino decisiones de diseno debiles que luego se corregiran en la rama `con-seguridad`.

## Dominio del ejemplo

El portal permite:

- inicio de sesion;
- cambio de rol de usuarios;
- carga de archivos de soporte;
- revision de archivos cargados;
- consulta de un tablero interno.

## Problemas de diseno que aparecen en esta rama

- mensajes de error demasiado detallados;
- exposicion de datos sensibles en las respuestas;
- cambios de rol sin control de privilegios;
- mezcla de responsabilidades entre estudiante, docente y administrador;
- carga de archivos sin validacion;
- ausencia de auditoria real;
- tablero interno expuesto a cualquier usuario.

## Ejecutar el ejemplo

```bash
python3 run_demo.py
```

## Recorrido sugerido en clase

1. Ejecutar `python3 run_demo.py`.
2. Identificar que decisiones de diseno hacen posible cada problema.
3. Pasar a la rama `con-seguridad`.
4. Comparar como cambia el mismo sistema cuando el diseno incorpora principios de seguridad.

## Siguiente paso

```bash
git checkout con-seguridad
git diff sin-seguridad..con-seguridad
```
