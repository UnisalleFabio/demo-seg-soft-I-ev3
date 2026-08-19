# Ejemplo guiado en Python para EV3

Estás en la rama `con-seguridad`.

Aquí vas a encontrar el mismo portal académico de la rama `sin-seguridad`, pero rediseñado con principios de diseño seguro.

## Qué deberías aprender en esta rama

Al recorrer este código deberías poder responder:

- qué cambio en el diseño del sistema frente a `sin-seguridad`;
- qué principio de seguridad justifica cada cambio;
- por qué una mejor implementación aquí nace de un mejor diseño previo.

## Qué hace el portal

El ejemplo incluye:

- inicio de sesión;
- cambio de rol de usuarios;
- carga de archivos de soporte;
- revisión de archivos cargados;
- consulta de auditoría.

## Principios de diseño seguro que puedes ubicar

| Principio | Dónde observarlo |
|---|---|
| Seguridad por diseño | `campus_portal/portal.py`, clase `CampusPortal` y su política de control |
| Defensa en profundidad | `login`, `upload_attachment`, `review_upload` |
| Principio de privilegio mínimo | matriz `PERMISSIONS` |
| Separación de responsabilidades | `student` sube, `teacher` revisa, `admin` cambia roles y lee auditoría |
| Falla segura | `_deny`, `_require_permission`, `login` y validaciones que niegan por defecto |
| Seguridad por defecto | `SecuritySettings` y `PERMISSIONS` con política de negación por defecto |
| Validación de entradas y salidas | `_validate_upload`, `_sanitize_filename`, `_public_user_view`, `_public_upload_view` |
| Minimización de superficie de ataque | tipos de archivo permitidos y operaciones explícitamente limitadas |
| Auditoría y monitoreo continuo | `_record_audit`, `_track_failed_login`, `get_security_dashboard` |

## Cómo explorar esta rama

Ejecuta el recorrido principal:

```bash
python3 run_demo.py
```

Si quieres verificar el comportamiento esperado:

```bash
python3 -m unittest discover -s tests
```

Mientras lo revisas, fíjate en estas preguntas:

- por qué el login ya no revela detalles innecesarios;
- por qué un estudiante no puede cambiar su propio rol;
- por qué ya no se acepta cualquier archivo;
- por qué la auditoría ya no está disponible para todos.

## Cómo compararla con la rama insegura

```bash
git checkout sin-seguridad
git checkout con-seguridad
git diff sin-seguridad..con-seguridad
```

## El agente de IA de la ronda 5

En `demo_agente_ia/` está la demostración del agente de soporte que opera este portal leyendo un ticket externo con instrucciones ocultas. Se ejecuta desde la raíz del repositorio con `python3 -B demo_agente_ia/agente_soporte.py`, y su [README](demo_agente_ia/README.md) explica qué demuestra y en qué momento conviene correrlo. En esta rama el ataque queda bloqueado y auditado.

## Idea clave

Este ejemplo busca que veas algo concreto: un mal diseño no se corrige solo con una buena implementación. Si el sistema nace con permisos excesivos, flujos mal separados o salidas demasiado expuestas, el código puede verse ordenado y seguir siendo inseguro. Esa es justamente la idea de `OWASP Top 10 A04:2021 Insecure Design`.

## Estructura del proyecto

```text
campus_portal/
  __init__.py
  data.py
  portal.py
demo_agente_ia/
  __init__.py
  agente_soporte.py
  ticket_soporte.txt
run_demo.py
tests/
  test_portal.py
```
