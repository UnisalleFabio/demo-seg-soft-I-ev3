# Demostración: un agente de IA opera el portal académico

Material de apoyo para la ronda 5 del encuentro sobre principios de diseño seguro. Este módulo vive dentro del mismo repositorio del portal y opera contra el código de la rama en la que esté situado el repositorio.

## Qué demuestra

Un asistente automático lee un ticket de soporte escrito por un tercero y, a partir de ese texto, decide qué operaciones ejecutar en el portal. El ticket trae instrucciones ocultas dentro de un comentario. Eso es una **inyección indirecta de prompt**.

El mismo agente, con el mismo ticket, se ejecuta contra las dos ramas del repositorio. En `sin-seguridad` el ataque funciona y se lleva las credenciales. En `con-seguridad` queda bloqueado y registrado. La conclusión es la tesis del encuentro: **el modelo es igual de ingenuo en los dos casos, lo que cambia es el diseño que lo rodea**.

## Advertencia honesta para decirla en clase

Aquí **no hay un modelo de lenguaje real**. La función `modelo_decide` es una simulación deliberadamente ingenua, escrita así para que la demostración no dependa de una llave de API ni de conexión a internet, y para que la salida sea siempre la misma. El comportamiento que reproduce sí está documentado en incidentes reales, y EchoLeak (CVE-2025-32711, junio de 2025) es el ejemplo que conviene citar. Conviene decirlo en voz alta: perder credibilidad en este punto cuesta caro justo cuando llega la mejor parte de la clase.

## Cómo ejecutarlo

Siempre desde la raíz del repositorio, primero contra una rama y luego contra la otra:

```bash
git checkout sin-seguridad
python3 -B demo_agente_ia/agente_soporte.py

git checkout con-seguridad
python3 -B demo_agente_ia/agente_soporte.py
```

Se recomienda usar siempre `python3 -B` para no arrastrar archivos `.pyc` de la rama anterior.

También acepta otro ticket como argumento, lo cual es útil si en clase los estudiantes dictan su propia instrucción oculta:

```bash
python3 -B demo_agente_ia/agente_soporte.py otro_ticket.txt
```

## Salidas verificadas

Ejecutado el 19 de agosto de 2026 contra las dos ramas.

**Rama `sin-seguridad`:**

```text
   change_role:
      ACEPTADA: rol student -> admin
   get_security_dashboard:
      ACEPTADA: el tablero devolvió credenciales -> ana/123456, luis/docente123, root/admin

   Rol de 'ana': admin
   Eventos de auditoría registrados: 0
```

**Rama `con-seguridad`:**

```text
   change_role:
      RECHAZADA: Operación rechazada
   get_security_dashboard:
      RECHAZADA: Operación rechazada

   Rol de 'ana': student
   Eventos de auditoría registrados: 2
      - change_role | denied | Operación no autorizada
      - read_audit_log | denied | Operación no autorizada
```

## Una nota si llegaste aquí antes de la clase

La ronda 5 del encuentro funciona mejor como sorpresa: el efecto depende de ver las dos ejecuciones una detrás de otra sin conocer el resultado. Si clonaste el repositorio antes de la sesión, te conviene dejar este módulo para después de esa ronda.
