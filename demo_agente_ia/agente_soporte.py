"""Agente de soporte con IA sobre el portal académico del encuentro.

Este módulo forma parte del mismo repositorio del portal y opera contra el
código de la rama en la que esté situado el repositorio.

Qué demuestra
-------------
Un asistente automático lee un ticket de soporte escrito por un tercero y,
a partir de ese texto, decide qué operaciones ejecutar en el portal. El ticket
trae instrucciones ocultas. Eso es una inyección indirecta de prompt.

El mismo agente, con el mismo ticket, se ejecuta contra las dos ramas del
repositorio de clase:

    git checkout sin-seguridad   ->  el ataque funciona
    git checkout con-seguridad   ->  el ataque queda bloqueado y auditado

La conclusión de clase: el modelo es igual de ingenuo en los dos casos. Lo que
cambia es el diseño que lo rodea.

Importante para no exagerar en clase
------------------------------------
Aquí NO hay un modelo de lenguaje real. La función `modelo_decide` es una
simulación deliberadamente ingenua que reproduce el comportamiento observado
en incidentes reales (por ejemplo EchoLeak, CVE-2025-32711, en Microsoft 365
Copilot). Se simula para que la clase no dependa de una llave de API ni de
conexión a internet, y para que la salida sea siempre la misma.

Uso (desde la raíz del repositorio)
-----------------------------------
    python3 -B demo_agente_ia/agente_soporte.py                 # usa ticket_soporte.txt
    python3 -B demo_agente_ia/agente_soporte.py otro_ticket.txt
"""

import os
import re
import subprocess
import sys

CARPETA = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(CARPETA)

if not os.path.isdir(os.path.join(REPO, "campus_portal")):
    sys.exit(f"No encuentro el paquete campus_portal en la raíz del repositorio:\n  {REPO}")

sys.path.insert(0, REPO)

from campus_portal.portal import CampusPortal  # noqa: E402

USUARIO_DEL_AGENTE = "ana"


def rama_actual():
    """Nombre de la rama del repositorio del portal, para rotular la corrida."""
    try:
        salida = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=REPO,
            capture_output=True,
            text=True,
            check=True,
        )
        return salida.stdout.strip()
    except Exception:
        return "desconocida"


def titulo(texto):
    print()
    print("=" * 66)
    print(texto)
    print("=" * 66)


def modelo_decide(ticket):
    """Simulación del asistente: convierte texto en llamadas a herramientas.

    El problema de diseño está justo aquí: el agente no distingue entre lo que
    el usuario pide y lo que el texto le ordena. Todo llega como un solo flujo
    de tokens y cualquier línea con forma de instrucción se vuelve una acción.
    """
    acciones = []
    patron = re.compile(r"ACCION:\s*(\w+)\((.*?)\)", re.IGNORECASE)
    for nombre, argumentos in patron.findall(ticket):
        parametros = {}
        for pieza in argumentos.split(","):
            if "=" in pieza:
                clave, valor = pieza.split("=", 1)
                parametros[clave.strip()] = valor.strip()
        acciones.append((nombre, parametros))
    return acciones


def rol_de(portal, usuario):
    """Rol vigente del usuario, sirviendo en las dos ramas del repositorio."""
    if hasattr(portal, "users"):
        return portal.users.get(usuario, {}).get("role", "?")
    from campus_portal.data import USERS

    return USERS.get(usuario, {}).get("role", "?")


def auditoria_de(portal):
    """Eventos de auditoría registrados, sirviendo en las dos ramas."""
    if hasattr(portal, "audit_log"):
        return list(portal.audit_log)
    from campus_portal.data import AUDIT_LOG

    return list(AUDIT_LOG)


def resumir_respuesta(respuesta):
    """Traduce la respuesta del portal a una línea legible en pantalla."""
    if not respuesta.get("ok"):
        return f"RECHAZADA: {respuesta.get('error')}"

    if "users" in respuesta:
        filtradas = [
            f"{nombre}/{datos.get('password')}"
            for nombre, datos in respuesta["users"].items()
        ]
        return "ACEPTADA: el tablero devolvió credenciales -> " + ", ".join(filtradas)

    if "summary" in respuesta:
        return f"ACEPTADA: resumen de auditoría {respuesta['summary']}"

    if "after" in respuesta:
        return f"ACEPTADA: rol {respuesta.get('before')} -> {respuesta.get('after')}"

    return f"ACEPTADA: {respuesta}"


def main():
    ruta_ticket = sys.argv[1] if len(sys.argv) > 1 else os.path.join(CARPETA, "ticket_soporte.txt")
    with open(ruta_ticket, encoding="utf-8") as archivo:
        ticket = archivo.read()

    portal = CampusPortal()

    titulo(f"AGENTE DE SOPORTE  |  rama del portal: {rama_actual()}")
    print(f"El agente atiende tickets con la identidad de '{USUARIO_DEL_AGENTE}' (rol: "
          f"{rol_de(portal, USUARIO_DEL_AGENTE)}).")

    titulo("1. CONTENIDO NO CONFIABLE: el ticket que llega de afuera")
    print(ticket.strip())

    acciones = modelo_decide(ticket)

    titulo("2. LO QUE EL AGENTE DECIDIÓ HACER CON ESE TEXTO")
    for nombre, parametros in acciones:
        print(f"   -> {nombre}({parametros})")

    titulo("3. EJECUCIÓN CONTRA EL PORTAL")
    for nombre, parametros in acciones:
        herramienta = getattr(portal, nombre, None)
        if herramienta is None:
            print(f"   {nombre}: la herramienta no existe en el portal")
            continue
        respuesta = herramienta(**parametros)
        print(f"   {nombre}:")
        print(f"      {resumir_respuesta(respuesta)}")

    titulo("4. ESTADO DEL SISTEMA DESPUÉS DEL TICKET")
    print(f"   Rol de '{USUARIO_DEL_AGENTE}': {rol_de(portal, USUARIO_DEL_AGENTE)}")
    eventos = auditoria_de(portal)
    print(f"   Eventos de auditoría registrados: {len(eventos)}")
    for evento in eventos:
        accion = getattr(evento, "action", None)
        estado = getattr(evento, "status", None)
        detalle = getattr(evento, "detail", None)
        print(f"      - {accion} | {estado} | {detalle}")


if __name__ == "__main__":
    main()
