"""Demostración rápida de la rama con seguridad."""

from pprint import pprint

from campus_portal.portal import CampusPortal


def print_step(title):
    print()
    print(f"=== {title} ===")


def main():
    portal = CampusPortal()

    print_step("1. Login con mensajes neutros y auditoría")
    pprint(portal.login("desconocido", "123"))
    pprint(portal.login("ana", "mala"))
    pprint(portal.login("ana", "123456"))

    print_step("2. Un estudiante intenta escalar privilegios y es bloqueado")
    pprint(portal.change_role("ana", "ana", "admin"))

    print_step("3. Se rechaza un archivo peligroso por tipo y tamaño")
    pprint(portal.upload_attachment("ana", "script.sh", "text/x-shellscript", 9_000_000))

    print_step("4. Se acepta un PDF válido y luego lo revisa un docente")
    pprint(portal.upload_attachment("ana", "constancia.pdf", "application/pdf", 320_000))
    pprint(portal.review_upload("luis", 0, "approved"))

    print_step("5. Solo admin puede ver la auditoría resumida")
    pprint(portal.get_security_dashboard("ana"))
    pprint(portal.get_security_dashboard("root"))


if __name__ == "__main__":
    main()
