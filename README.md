# Ejemplo guiado en Python para EV3

Este repositorio contiene un ejemplo guiado para el EV3 de `Seguridad de Software I`.

La idea didáctica es comparar el mismo portal académico pequeño en dos ramas:

- `sin-seguridad`: implementación deliberadamente débil.
- `con-seguridad`: implementación endurecida con principios de diseño seguro comentados en el código.

## Flujo sugerido

1. Revisar la rama `sin-seguridad`.
2. Identificar decisiones de diseño débiles.
3. Cambiar a `con-seguridad`.
4. Comparar qué principios se aplicaron y por qué.

## Comandos útiles

```bash
git branch
git checkout sin-seguridad
git checkout con-seguridad
git diff sin-seguridad..con-seguridad
```
