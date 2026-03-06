# Ejemplo guiado en Python para EV3

Estas en la rama `sin-seguridad`.

Aqui vas a encontrar una version intencionalmente insegura de un portal academico pequeno. La idea no es que mires "codigo malo" por estilo, sino decisiones de diseno debiles que luego podras contrastar con la rama `con-seguridad`.

## Que deberias observar en esta rama

Mientras recorres el ejemplo, intenta detectar:

- que informacion se expone de mas;
- que operaciones tienen permisos excesivos;
- donde se mezclan responsabilidades que deberian separarse;
- que entradas aceptan mas de lo necesario;
- que eventos importantes no quedan auditados correctamente.

## Que hace el portal

El ejemplo incluye:

- inicio de sesion;
- cambio de rol de usuarios;
- carga de archivos de soporte;
- revision de archivos cargados;
- consulta de un tablero interno.

## Problemas de diseno presentes

- mensajes de error demasiado detallados;
- exposicion de datos sensibles en las respuestas;
- cambios de rol sin control de privilegios;
- mezcla de responsabilidades entre estudiante, docente y administrador;
- carga de archivos sin validacion;
- ausencia de auditoria real;
- tablero interno expuesto a cualquier usuario.

## Como explorarlo

Ejecuta el recorrido principal:

```bash
python3 run_demo.py
```

Mientras lo haces, preguntate:

- que principio de diseno seguro esta ausente aqui;
- que parte del sistema esta demasiado expuesta;
- por que este problema no se arregla solo "escribiendo mejor codigo".

## Siguiente paso

Cuando termines de identificar problemas, compara con la rama segura:

```bash
git checkout con-seguridad
git diff sin-seguridad..con-seguridad
```

## Idea clave

Esta rama te ayuda a ver algo importante para el EV3: muchos problemas no nacen de un error pequeno de implementacion, sino de decisiones de diseno inseguras. Por eso OWASP Top 10 A04:2021 habla de `Insecure Design`.
