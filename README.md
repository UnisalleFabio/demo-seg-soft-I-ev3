# Ejemplo guiado en Python para EV3

Estas en la rama `con-seguridad`.

Aqui vas a encontrar el mismo portal academico de la rama `sin-seguridad`, pero redisenado con principios de diseno seguro.

## Que deberias aprender en esta rama

Al recorrer este codigo deberias poder responder:

- que cambio en el diseno del sistema frente a `sin-seguridad`;
- que principio de seguridad justifica cada cambio;
- por que una mejor implementacion aqui nace de un mejor diseno previo.

## Que hace el portal

El ejemplo incluye:

- inicio de sesion;
- cambio de rol de usuarios;
- carga de archivos de soporte;
- revision de archivos cargados;
- consulta de auditoria.

## Principios de diseno seguro que puedes ubicar

| Principio | Donde observarlo |
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

## Como explorar esta rama

Ejecuta el recorrido principal:

```bash
python3 run_demo.py
```

Si quieres verificar el comportamiento esperado:

```bash
python3 -m unittest discover -s tests
```

Mientras lo revisas, fijate en estas preguntas:

- por que el login ya no revela detalles innecesarios;
- por que un estudiante no puede cambiar su propio rol;
- por que ya no se acepta cualquier archivo;
- por que la auditoria ya no esta disponible para todos.

## Como compararla con la rama insegura

```bash
git checkout sin-seguridad
git checkout con-seguridad
git diff sin-seguridad..con-seguridad
```

## Idea clave

Este ejemplo busca que veas algo concreto: un mal diseno no se corrige solo con una buena implementacion. Si el sistema nace con permisos excesivos, flujos mal separados o salidas demasiado expuestas, el codigo puede verse ordenado y seguir siendo inseguro. Esa es justamente la idea de `OWASP Top 10 A04:2021 Insecure Design`.

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
