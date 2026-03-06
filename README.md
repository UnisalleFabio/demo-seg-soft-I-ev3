# Ejemplo guiado en Python para EV3

Estás en la rama `sin-seguridad`.

Aquí vas a encontrar una versión intencionalmente insegura de un portal académico pequeño. La idea no es que mires "código malo" por estilo, sino decisiones de diseño débiles que luego podrás contrastar con la rama `con-seguridad`.

## Qué deberías observar en esta rama

Mientras recorres el ejemplo, intenta detectar:

- qué información se expone de más;
- qué operaciones tienen permisos excesivos;
- dónde se mezclan responsabilidades que deberían separarse;
- qué entradas aceptan más de lo necesario;
- qué eventos importantes no quedan auditados correctamente.

## Qué hace el portal

El ejemplo incluye:

- inicio de sesión;
- cambio de rol de usuarios;
- carga de archivos de soporte;
- revisión de archivos cargados;
- consulta de un tablero interno.

## Problemas de diseño presentes

- mensajes de error demasiado detallados;
- exposición de datos sensibles en las respuestas;
- cambios de rol sin control de privilegios;
- mezcla de responsabilidades entre estudiante, docente y administrador;
- carga de archivos sin validación;
- ausencia de auditoría real;
- tablero interno expuesto a cualquier usuario.

## Cómo explorarlo

Ejecuta el recorrido principal:

```bash
python3 run_demo.py
```

Mientras lo haces, pregúntate:

- qué principio de diseño seguro está ausente aquí;
- qué parte del sistema está demasiado expuesta;
- por qué este problema no se arregla solo "escribiendo mejor código".

## Siguiente paso

Cuando termines de identificar problemas, compara con la rama segura:

```bash
git checkout con-seguridad
git diff sin-seguridad..con-seguridad
```

## Idea clave

Esta rama te ayuda a ver algo importante para el EV3: muchos problemas no nacen de un error pequeño de implementación, sino de decisiones de diseño inseguras. Por eso OWASP Top 10 A04:2021 habla de `Insecure Design`.
