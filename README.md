# Ejemplo guiado en Python para EV3

Esta rama contiene la version endurecida del mismo portal academico usado en la rama `sin-seguridad`.

El objetivo didactico es comparar exactamente el mismo dominio con dos enfoques:

- `sin-seguridad`: decisiones de diseno debiles.
- `con-seguridad`: decisiones de diseno alineadas con principios de seguridad.

## Dominio del ejemplo

El portal permite:

- inicio de sesion;
- cambio de rol de usuarios;
- carga de archivos de soporte;
- revision de archivos cargados;
- consulta de auditoria.

## Principios de diseno seguro implementados

| Principio | Donde verlo |
|---|---|
| Seguridad por diseno | `campus_portal/portal.py`, clase `CampusPortal` y su politica de control |
| Defensa en profundidad | `login`, `upload_attachment`, `review_upload` |
| Principio de privilegio minimo | matriz `PERMISSIONS` |
| Separacion de responsabilidades | `student` sube, `teacher` revisa, `admin` cambia roles y lee auditoria |
| Falla segura | `_deny`, `_require_permission`, `login` y validaciones que niegan por defecto |
| Seguridad por defecto | `SecuritySettings` y `PERMISSIONS` con politica de negacion por defecto |
| Validacion de entradas y salidas | `_validate_upload`, `_sanitize_filename`, `_public_user_view`, `_public_upload_view` |
| Minimizacion de superficie de ataque | tipos de archivo permitidos y operaciones explicitamente limitadas |
| Auditoria y monitoreo continuo | `_record_audit`, `_track_failed_login`, `get_security_dashboard` |

## Por que este ejemplo sirve para EV3

La comparacion entre ramas permite explicar que un mal diseno no se corrige solo con una buena implementacion. Si el sistema expone demasiados permisos, mezcla responsabilidades o filtra mas informacion de la necesaria, el codigo puede estar ordenado y aun asi seguir siendo inseguro. Esa es justamente la idea que OWASP Top 10 A04:2021 recoge en `Insecure Design`.

## Ejecutar el ejemplo

```bash
python3 run_demo.py
```

## Ejecutar pruebas basicas

```bash
python3 -m unittest discover -s tests
```

## Comparar ramas

```bash
git checkout sin-seguridad
git checkout con-seguridad
git diff sin-seguridad..con-seguridad
```

## Recorrido sugerido en clase

1. Ejecutar `python3 run_demo.py` en `sin-seguridad`.
2. Pedir al grupo que identifique errores de diseno.
3. Cambiar a `con-seguridad`.
4. Volver a ejecutar `python3 run_demo.py`.
5. Relacionar cada cambio con un principio de diseno seguro.

## Estructura del proyecto

```text
campus_portal/
  __init__.py
  data.py
  portal.py
run_demo.py
tests/
  test_portal.py
```
