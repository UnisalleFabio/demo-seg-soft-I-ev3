"""Demostración rápida de la rama sin seguridad."""

from pprint import pprint

from campus_portal.portal import CampusPortal


def print_step(title):
    print()
    print(f"=== {title} ===")


def main():
    portal = CampusPortal()

    print_step("1. Flujo de inicio de sesión")
    pprint(portal.login("desconocido", "123"))
    pprint(portal.login("ana", "123456"))

    print_step("2. Cambio de rol de usuario")
    pprint(portal.change_role("ana", "ana", "admin"))

    print_step("3. Carga de archivo adjunto")
    pprint(portal.upload_attachment("ana", "script.sh", "text/x-shellscript", 9_000_000))

    print_step("4. Revisión de archivo cargado")
    pprint(portal.review_upload("ana", 0, "approved"))

    print_step("5. Consulta de tablero interno")
    pprint(portal.get_security_dashboard("ana"))


if __name__ == "__main__":
    main()
